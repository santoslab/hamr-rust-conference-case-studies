# BASS with Integration Constraints (`bass_ic`)

A copy of [BASS](../bass/readme.md) extended with GUMBO **integration constraints** on the
connections between the firewalls and ArduPilot. It exists to illustrate how HAMR turns
integration constraints into Verus contracts (e.g. for screenshots). It is not one of the
paper's measured case studies.

Everything else is unchanged from `bass`: the model's other contracts, and the firewalls' and
ModeManager's behavior and test code. The only new behavior code is a small ArduPilot stand-in
(see [ArduPilot behavior](#ardupilot-behavior)).

Status: `make verus` succeeds for every crate, including the system-verification crate, and
`make test` passes (118 tests; see [Testing](#testing)).

**Contents**

- [What was added](#what-was-added)
  - [1. Library predicates (`GumboLib.sysml` L32–L44)](#1-library-predicates-gumbolibsysml-l32l44)
  - [2. Integration constraints](#2-integration-constraints)
  - [3. A composition, for the connection checks (`SW.sysml` L461–L477)](#3-a-composition-for-the-connection-checks-swsysml-l461l477)
- [ArduPilot behavior](#ardupilot-behavior)
- [Testing](#testing)
- [Regenerating and verifying](#regenerating-and-verifying)

## What was added

### 1. Library predicates ([`GumboLib.sysml` L32–L44](sysml/GumboLib.sysml#L32-L44))

These are the frame properties that BASS's existing compute contracts already encode, stated as
reusable GUMBO functions:

| Predicate | Meaning | Derived from |
|:--|:--|:--|
| `rxShouldPass(v)` | not malformed **and** IPv4 **and** TCP **and** whitelisted port | the condition of RC_INSPECTA_00_HLR_9 (minus the mode) |
| `rxShouldDrop(v)` | malformed **or** IPv6 **or** ARP **or** (IPv4 TCP on a non-whitelisted port) | the disjunction of HLR_2, HLR_4, HLR_6 and HLR_8 |
| `txExpected(v)` | IPv4 **or** ARP | an assumption about ArduPilot's network stack (never IPv6) |

### 2. Integration constraints

An integration *guarantee* on an out port is an obligation on the sender. An integration *assume* on
an in port is what the receiver may rely on. Each row links the GUMBO clause and the Verus
contract HAMR generates from it.

| Connection | GUMBO clause | Generated Verus contract |
|:--|:--|:--|
| RxFirewall → ArduPilot | RxFirewall **guarantee** `RxOut_OnlyPermitted`: `rxShouldPass(EthernetFramesRxOut)` — [`SW.sysml` L108–L109](sysml/SW.sysml#L108-L109) | `requires` of `put_EthernetFramesRxOut` — [`FirewallRx_FirewallRx_api.rs` L79–L81](hamr/microkit_mcs/crates/FirewallRx_FirewallRx/src/bridge/FirewallRx_FirewallRx_api.rs#L79-L81) |
| | ArduPilot **assume** `RxIn_NoBlockedFrames`: `not rxShouldDrop(EthernetFramesRx)` — [`SW.sysml` L249–L250](sysml/SW.sysml#L249-L250) | `ensures` of `get_EthernetFramesRx` — [`ArduPilot_ArduPilot_api.rs` L75–L78](hamr/microkit_mcs/crates/ArduPilot_ArduPilot/src/bridge/ArduPilot_ArduPilot_api.rs#L75-L78) |
| ArduPilot → TxFirewall | ArduPilot **guarantee** `TxOut_IPv4OrARP`: `txExpected(EthernetFramesTx)` — [`SW.sysml` L252–L253](sysml/SW.sysml#L252-L253) | `requires` of `put_EthernetFramesTx` — [`ArduPilot_ArduPilot_api.rs` L57–L59](hamr/microkit_mcs/crates/ArduPilot_ArduPilot/src/bridge/ArduPilot_ArduPilot_api.rs#L57-L59) |
| | TxFirewall **assume** `TxIn_IPv4OrARP`: `txExpected(EthernetFramesTxIn)` — [`SW.sysml` L192–L193](sysml/SW.sysml#L192-L193) | `ensures` of `get_EthernetFramesTxIn` — [`FirewallTx_FirewallTx_api.rs` L117–L120](hamr/microkit_mcs/crates/FirewallTx_FirewallTx/src/bridge/FirewallTx_FirewallTx_api.rs#L117-L120) |
| TxFirewall → driver | TxFirewall **guarantee** `TxOut_OnlyPermitted`: not malformed and `txExpected(EthernetFramesTxOut)` — [`SW.sysml` L195–L197](sysml/SW.sysml#L195-L197) | `requires` of `put_EthernetFramesTxOut` — [`FirewallTx_FirewallTx_api.rs` L83–L85](hamr/microkit_mcs/crates/FirewallTx_FirewallTx/src/bridge/FirewallTx_FirewallTx_api.rs#L83-L85) |

The library predicates become Verus `open spec fn`s in the generated `GumboLib` crate:
[`GumboLib/src/lib.rs` L196–L214](hamr/microkit_mcs/crates/GumboLib/src/lib.rs#L196-L214).

How to read the generated contracts:

- **Guarantee → `requires` on `put_`.** The developer's code can send only values that
  satisfy the guarantee. Verus checks this at every `put_` call in the component's code. For the
  RxFirewall and TxFirewall, the existing code (unchanged from `bass`) already sends only under
  those conditions, so it verifies as is. As a check, making the RxFirewall also forward ARP
  frames is rejected at the `put_EthernetFramesRxOut` precondition.
- **Assume → `ensures` on `get_`.** The developer's code may rely on every received value
  satisfying the assume. For an event-data port, the assume applies only when a frame is present
  (`res.is_none() || ...`).

### 3. A composition, for the connection checks ([`SW.sysml` L461–L477](sysml/SW.sysml#L461-L477))

The per-component contracts above say nothing about whether the sender's guarantee is strong enough
for the receiver's assume. HAMR checks that per connection in the system-verification crate,
which it generates only for a model with a GUMBO `composition`. So `bass_ic` adds a minimal one
on `seL4_i` (components and schema only, no properties). Its schema follows the user-land schedule
order (the processes' `Domain`s): driver; rx; tx; ap; mm.

For each connection into a port with an integration assume, HAMR emits a Verus proof function
stating guarantee ⇒ assume over the value the connection carries:

| Connection | Verus VC | Spec functions it uses |
|:--|:--|:--|
| RxFirewall → ArduPilot: `rxShouldPass` ⇒ `not rxShouldDrop` | [`vc_integration.rs` L34–L43](hamr/microkit_mcs/crates/sys_nominal_proof/src/vc_integration.rs#L34-L43) | [rx guarantee](hamr/microkit_mcs/crates/sys_nominal_proof/src/contracts.rs#L168-L175), [ap assume](hamr/microkit_mcs/crates/sys_nominal_proof/src/contracts.rs#L19-L26) |
| ArduPilot → TxFirewall: `txExpected` ⇒ `txExpected` | [`vc_integration.rs` L23–L32](hamr/microkit_mcs/crates/sys_nominal_proof/src/vc_integration.rs#L23-L32) | [ap guarantee](hamr/microkit_mcs/crates/sys_nominal_proof/src/contracts.rs#L28-L35), [tx assume](hamr/microkit_mcs/crates/sys_nominal_proof/src/contracts.rs#L269-L276) |

The RxFirewall → ArduPilot VC is the interesting one. The sender's guarantee is stated as a
conjunction of what should get through. The receiver's assume is stated as the negation of a
disjunction of what must not. They are different formulas, and Verus discharges the implication
from the data-type definitions (an `InternetProtocol` is IPv4 or IPv6; a `FrameProtocol` is TCP
or ARP). Both VCs verify with an empty proof body.

There is no VC for TxFirewall → driver, because the driver declares no integration assume.

## ArduPilot behavior

ArduPilot is not implemented in `bass`. Here it gets a minimal stand-in for its network stack:
each frame received from the RxFirewall is sent back out through the TxFirewall
([`ArduPilot_ArduPilot_app.rs` L38–L46](hamr/microkit_mcs/crates/ArduPilot_ArduPilot/src/component/ArduPilot_ArduPilot_app.rs#L38-L46)):

```rust
if let Some(frame) = api.get_EthernetFramesRx() {
  api.put_EthernetFramesTx(frame);
}
```

This makes a small proof chained through an integration assume. `put_EthernetFramesTx` requires
the frame to be IPv4 or ARP (ArduPilot's guarantee). Verus proves that from what
`get_EthernetFramesRx` ensures: the frame is not one the RxFirewall must drop, so it is not IPv6.

## Testing

`make test` passes for every crate: ArduPilot (4 tests), FirewallRx (43), FirewallTx (38),
LowLevelEthernetDriver (4) and ModeManager (29).

Integration constraints also reach testing. HAMR includes a component's out-port integration
guarantees in its compute post-condition oracle
([`FirewallTx_FirewallTx_GUMBOX.rs` L262–L274](hamr/microkit_mcs/crates/FirewallTx_FirewallTx/src/bridge/FirewallTx_FirewallTx_GUMBOX.rs#L262-L274)),
which every unit and property-based test of the component checks:

```rust
// I-Guar-Guard: Integration constraints for FirewallTx's outgoing ports
let r0: bool = I_Guar_Guard_EthernetFramesTxOut(api_EthernetFramesTxOut);
// CEP-Guar: guarantee clauses of FirewallTx's compute entrypoint
let r1: bool = compute_CEP_T_Guar(...);
return r0 && r1;
```

So a test in which the TxFirewall forwards a malformed frame fails on `TxOut_OnlyPermitted` as
well as on the compute contract.

## Regenerating and verifying

```sh
sysml/bin/run-hamr.cmd                        # HAMR codegen (Verus 0.2026.09.06)
make -C hamr/microkit_mcs verus               # all crates, then the system-verification crate
make -C hamr/microkit_mcs test                # unit and property-based tests
```
