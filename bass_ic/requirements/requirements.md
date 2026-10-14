# BASS Isolate-Ethernet-Simple — System Requirements

This file contains the system-level requirements for the isolate-ethernet-simple
system, a simplified rendition of the INSPECTA Open Platform architecture in which
two firewall components mediate all ethernet traffic between a mocked legacy
autopilot (`ArduPilot`) and the external network — see `requirements/conops.md`
for the full Concept of Operations and domain model this document traces to.

**Provenance.** These requirements were **reverse-engineered on 2026-07-25** from
the GUMBO compute contracts in `sysml/SW.sysml` (guarantee labels
`RC_INSPECTA_00_HLR_N`), the GUMBO library `sysml/GumboLib.sysml`, and the
component implementations/tests. Each firewall requirement below cites its GUMBO
guarantee label and, in brackets, the full-system source HLR ID quoted in that
guarantee's docstring (`RC_INSPECTA_00-HLR-N`). Requirement text follows the
**formal predicates**, not the docstrings, where the two differ (see
Reverse-Engineering Observations at the end).

**Revision (CR-01).** `[Revision, CR-01, 2026-07-26 — see
action-requests/CR-01-add-RTL-mode/]` The system is now **cyber-mode aware**:
a new Mode Manager component broadcasts the system mode (`Init`, `Normal`,
`RTL`), both firewalls detect (mocked) attack evidence and report an attack
status to the Mode Manager, and both firewalls gate their pass-through behavior
on the current mode. New requirements: `Req_Mode_*` (mode management,
ModeManager) and `Req_Detect_*` (attack detection, firewalls), plus the two
mode-gate requirements `Req_Rx_ModeGate` / `Req_Tx_ModeGate`. The three
**pass-through** requirements (`Req_Rx_Allow`, `Req_Tx_Allow_ARP`,
`Req_Tx_Allow_IPv4`) are re-scoped to Normal mode. The **drop** and
**no-input** requirements remain deliberately **unconditional**: in Init and
RTL modes every frame is dropped, so those requirements hold in every mode —
conditioning them on Normal would weaken them without need. `ASSUMED: plan §4
F1 said "re-scope all existing guarantees"; executed as re-scope pass-through
only, keep drops/no-input unconditional — a strictly stronger form (deviation
recorded in the CR-01 change report; rapid profile, 2026-07-26).`

## System Boundary and External Interfaces

### Inputs

- Inbound ethernet frames arriving at the platform's physical network interface,
  entering the system through `LowLevelEthernetDriver` (mocked — see
  `Req_Transport`).

### Outputs

- Outbound ethernet frames leaving through the same interface, after outbound
  mediation (mocked at the driver — see `Req_Transport`).

There are no other external interfaces. Ground control stations exist only at
concept level, as the remote endpoints of the mediated traffic.

## Data Requirements

- The system shall process a single data item, the **ethernet frame**
  (`SW::StructuredEthernetMessage_i`), consisting of a fixed 1600-byte raw payload
  (`rawMessage`) plus pre-decoded classification attributes: `malformedFrame`
  (boolean), `internetProtocol` (`IPV4 | IPV6`), `frameProtocol` (`TCP | ARP`),
  `portIsWhitelisted` (boolean), and `arpType` (`REQUEST | REPLY | NA`). See
  `requirements/data-dictionary.md`.
- Every frame shall satisfy the classification invariant
  (`relateFrameProtocolToArpType`): TCP frames carry `arpType == NA`; ARP frames
  carry `arpType ∈ {REQUEST, REPLY}`.
- Classification attributes are trusted as given; no component parses the raw
  bytes (`conops.md` §9 Assumption 1) — with one CR-01 exception: the TX
  Firewall reads (only) byte 0 of `rawMessage` as the mocked geofence-violation
  indicator (`Req_Detect_Tx`).
- `[Revision, CR-01, 2026-07-26]` The system shall additionally process two
  enumerated data items: the **system mode** (`SW::Mode`: `Init`, `Normal`,
  `RTL`) broadcast by the Mode Manager, and the **attack status**
  (`SW::AttackStatus`: `OK`, `Attack`) reported by each firewall. Both are
  carried on **DataPorts** (sampled, continuously-valid values — RD-4 in the
  CR-01 change plan, per `hamr-sysml-patterns.md` §1), unlike the frame ports,
  which remain EventDataPorts.

## System Requirements

Inbound mediation (RX Firewall; "received frame" = the frame present on the RX
Firewall's input on a given dispatch):

- **Req_Rx_Allow** *(revised, CR-01 — Normal mode only)*: **In Normal mode**,
  every received frame that is well-formed (not malformed), IPv4, TCP, and
  whose port is whitelisted shall be delivered toward `ArduPilot` unchanged.
  *(GUMBO `RC_INSPECTA_00_HLR_9` [RC_INSPECTA_00-HLR-8])*
- **Req_Rx_Drop_Malformed**: Every received frame that is malformed shall be
  dropped. *(GUMBO `RC_INSPECTA_00_HLR_2` [RC_INSPECTA_00-HLR-1])*
- **Req_Rx_Drop_IPv6**: Every received IPv6 frame shall be dropped.
  *(GUMBO `RC_INSPECTA_00_HLR_4` [RC_INSPECTA_00-HLR-2])*
- **Req_Rx_Drop_ARP**: Every received ARP frame shall be dropped.
  *(GUMBO `RC_INSPECTA_00_HLR_6` [RC_INSPECTA_00-HLR-4])*
- **Req_Rx_Drop_NonWhitelisted**: Every received IPv4 TCP frame whose port is not
  whitelisted shall be dropped. *(GUMBO `RC_INSPECTA_00_HLR_8`
  [RC_INSPECTA_00-HLR-6])*
- **Req_Rx_NoInput**: When no frame is received on a dispatch, no frame shall be
  emitted toward `ArduPilot` on that dispatch. *(GUMBO `RC_INSPECTA_00_HLR_1`
  [RC_INSPECTA_00-HLR-1])*
- **Req_Rx_ModeGate** *(new, CR-01)*: When the current mode is Init or RTL, no
  frame shall be emitted toward `ArduPilot`, regardless of input. *(GUMBO
  `CR01_Rx_ModeGate`)*

The four RX drop requirements above are **unconditional** — they hold in every
mode (in Init/RTL, `Req_Rx_ModeGate` drops those frames along with everything
else; in Normal, the baseline policy applies).

Outbound mediation (TX Firewall; "received frame" = the frame present on the TX
Firewall's input on a given dispatch):

- **Req_Tx_Allow_ARP** *(revised, CR-01 — Normal mode only)*: **In Normal
  mode**, every received frame that is well-formed and ARP shall be transmitted
  toward the network unchanged. *(GUMBO `RC_INSPECTA_00_HLR_7`
  [RC_INSPECTA_00-HLR-7])*
- **Req_Tx_Allow_IPv4** *(revised, CR-01 — Normal mode only)*: **In Normal
  mode**, every received frame that is well-formed and IPv4 shall be
  transmitted toward the network unchanged. *(GUMBO `RC_INSPECTA_00_HLR_12`
  [RC_INSPECTA_00-HLR-12])*
- **Req_Tx_Drop**: Every received frame that is malformed, or that is neither
  IPv4 nor ARP (i.e., a well-formed IPv6 non-ARP frame), shall be dropped.
  *(GUMBO `RC_INSPECTA_00_HLR_14` [RC_INSPECTA_00-HLR-14]; text follows the
  formal predicate — see Observation 1)*
- **Req_Tx_NoInput**: When no frame is received on a dispatch, no frame shall be
  transmitted on that dispatch. *(GUMBO `RC_INSPECTA_00_HLR_16`
  [RC_INSPECTA_00-HLR-16])*
- **Req_Tx_ModeGate** *(new, CR-01)*: When the current mode is Init or RTL, no
  frame shall be transmitted toward the network, regardless of input. *(GUMBO
  `CR01_Tx_ModeGate`)*

`Req_Tx_Drop` and `Req_Tx_NoInput` are **unconditional** — they hold in every
mode, for the same reason as the RX drop requirements.

Attack detection (both firewalls; detection is **observational and
mode-independent** — evidence is monitored in every mode, including while
frames are being dropped in Init/RTL. `ASSUMED: mode-independent detection —
the sketch does not restrict detection by mode, and change-plan finding 10
records detection as observational (rapid profile, 2026-07-26).`):

- **Req_Detect_Rx** *(new, CR-01)*: The RX Firewall shall maintain a cumulative
  count of malformed received frames since initialization (saturating at 6, per
  RD-1) and shall report attack status `Attack` when that count exceeds five,
  and `OK` otherwise. Once the threshold is crossed the count can never
  decrease, so the RX attack report is latched by construction. *(GUMBO
  `CR01_Rx_Count`, `CR01_Rx_Detect`)*
- **Req_Detect_Tx** *(new, CR-01)*: The TX Firewall shall report attack status
  `Attack` on every dispatch in which the received frame's `rawMessage` byte 0
  equals 0 (the mocked geofence-violation indicator, per RD-2), and `OK` on
  every other dispatch (including no-input dispatches). The TX report is
  per-dispatch (transient); persistence of the response is provided by the Mode
  Manager's RTL latch, not by the TX Firewall. `ASSUMED: per-dispatch TX
  detection with no TX-side latch, per change-plan §9 acceptance criteria
  ("both report OK otherwise"); the static schedule guarantees the Mode Manager
  samples every written attack-status value exactly once, so a one-dispatch
  Attack pulse cannot be missed (rapid profile, 2026-07-26).` *(GUMBO
  `CR01_Tx_Detect`)*

Mode management (Mode Manager, new component, CR-01):

- **Req_Mode_Init** *(new, CR-01)*: The system shall start in Init mode: the
  Mode Manager shall initialize its broadcast mode to `Init` before any
  component's first compute dispatch.
- **Req_Mode_Normal** *(new, CR-01)*: The Mode Manager shall count its
  activations (compute dispatches), saturating at 10; while in Init mode with
  no attack reported, it shall remain in Init until the count reaches 10 and
  shall broadcast `Normal` from the 10th activation onward. `ASSUMED:
  "after 10 activations" interpreted as: the broadcast value becomes Normal on
  the 10th compute dispatch; counting the DataPort initialization value, Init
  is thus observable for exactly 10 mode samples (initialize + dispatches 1–9)
  — matches change-plan §9 "transitions to Normal at the 10th activation"
  (rapid profile, 2026-07-26).`
- **Req_Mode_RTL** *(new, CR-01)*: When either firewall's reported attack
  status reads `Attack`, the Mode Manager shall broadcast `RTL` from that
  dispatch onward. RTL entry takes precedence over the Init→Normal transition
  and is reachable from both Init and Normal. `ASSUMED: RTL reachable directly
  from Init (the sketch does not restrict detection-triggered transition to
  Normal mode); on a dispatch where the activation count reaches 10 and an
  attack is reported, RTL wins (rapid profile, 2026-07-26).`
- **Req_Mode_Absorbing** *(new, CR-01)*: RTL mode is absorbing: once entered,
  the system remains in RTL until restart (RD-3).
- **Req_Mode_Broadcast** *(new, CR-01)*: On every dispatch the Mode Manager
  shall broadcast its current mode on its mode output; mode-aware components
  (both firewalls) sample this value each dispatch.

Transport and autonomy (mocked components — intended roles, not contracted or
implemented; see Observation 4):

- **Req_Transport** *(mocked)*: `LowLevelEthernetDriver` shall forward each frame
  received from the physical network interface to the RX Firewall, and shall
  transmit each frame received from the TX Firewall on the physical network
  interface.
- **Req_Autonomy** *(mocked)*: `ArduPilot` shall consume the frames delivered by
  the RX Firewall and shall produce the outbound frames handed to the TX
  Firewall, standing in for the legacy autonomy application.

Platform:

- **Req_Timing** *(revised, CR-01 — Mode Manager added)*:
  `LowLevelEthernetDriver`, RX Firewall, TX Firewall, `ArduPilot`, and the Mode
  Manager shall each be dispatched periodically with a period of 1000 ms.
- **Req_Isolation** *(revised, CR-01 — Mode Manager added)*: Each of the five
  components shall execute in its own seL4 protection domain (one thread per
  process; scheduling domains 2–6), so that all inter-component communication
  flows through the modeled port connections.

## Design Expectations

`[Revision, CR-01, 2026-07-26]` The system is a mediation ring of five periodic
Thread components, one per process/protection domain, all bound to a single
`ZCU102_Processor` (1000 ms major frame):

- **LowLevelEthernetDriver** (domain 2, mocked) — network boundary; one inbound
  output, one outbound input.
- **RX Firewall** (`Firewall_Rx_i`, domain 3) — inbound mediation;
  `EthernetFramesRxIn` → `EthernetFramesRxOut`; CR-01: mode input
  `CurrentMode`, attack-status output `AttackStatusRx`, malformed-frame
  counting.
- **TX Firewall** (`Firewall_Tx_i`, domain 4) — outbound mediation;
  `EthernetFramesTxIn` → `EthernetFramesTxOut`; CR-01: mode input
  `CurrentMode`, attack-status output `AttackStatusTx`, geofence-mock
  detection.
- **ArduPilot** (domain 5, mocked) — the protected legacy application.
- **Mode Manager** (`ModeManager_i`, domain 6, new in CR-01) — consumes
  `AttackStatusRx`/`AttackStatusTx`, broadcasts `CurrentMode`.

Frame ports are EventDataPorts carrying `StructuredEthernetMessage_i`; the
CR-01 mode and attack-status ports are **DataPorts** carrying `SW::Mode` /
`SW::AttackStatus` (RD-4). Frames that pass a firewall are copied through
unchanged — mediation is pass/drop only, with no frame rewriting. The new
topology contains a sampled feedback cycle (firewalls → Mode Manager →
firewalls), legal for DataPorts; mode reaction lags detection by at most one
major frame, with the exact lag fixed by the schedule position of domain 6
(change-plan finding 7). Components execute under a static cyclic schedule
(`microkit.schedule.xml`: 100 ms slots for domains 2–6 within the 1000 ms major
frame).

## Reverse-Engineering Observations

Recorded rather than silently fixed; requirement text above follows the formal
predicates.

1. **`Req_Tx_Drop` docstring vs. predicate.** The docstring of
   `RC_INSPECTA_00_HLR_14` says "malformed ARP frame or malformed TCP frame", but
   the formal predicate is `(not isIPV4 and not isARP) or isMalformedFrame` — it
   additionally drops *well-formed* IPv6 non-ARP frames. The requirement follows
   the predicate.
2. **`Req_Rx_Drop_ARP` docstring vs. predicate.** The docstring of
   `RC_INSPECTA_00_HLR_6` says "Ipv4 frame whose protocol is ARP", but the
   predicate tests only `isARP` — all ARP frames are dropped regardless of
   internet protocol. The effect is the same (IPv6 frames are already dropped by
   `RC_INSPECTA_00_HLR_4`), but the requirement follows the broader predicate.
3. **RX label/source-HLR offset and numbering gaps.** In the RX contract, the
   guarantee labels and the source HLR IDs quoted in their docstrings are offset
   (`HLR_2` cites HLR-1, `HLR_4` cites HLR-2, `HLR_6` cites HLR-4, `HLR_8` cites
   HLR-6, `HLR_9` cites HLR-8); the TX labels match their cited HLRs. Gaps in the
   numbering (no HLR_3/5/10/11/13/15) reflect the full-system requirement set
   this example was simplified from.
4. **Mocked components.** `LowLevelEthernetDriver` and `ArduPilot` carry no GUMBO
   contracts, and their current implementations are no-op stubs (log only, no
   port I/O) — `Req_Transport` and `Req_Autonomy` state intended roles and are
   neither verified nor implemented. Note the consequence: until they are
   implemented, no frames actually flow end-to-end at runtime; firewall behavior
   is exercised by the per-component test/verification infrastructure.
5. **No port-level integration constraints.** The model contains no GUMBO
   `integration` blocks — the only model-level value constraint is the data-type
   invariant `relateFrameProtocolToArpType`. Per `hamr-sysml-patterns.md` §2, a
   `SysGUMBOIntegrationCheck` run on this model is **vacuous by design** (zero
   receiver-side assumes ⇒ zero verification conditions), and the system currently
   has no machine-checked cross-component argument; the security policy is carried
   entirely by the two firewalls' compute contracts.
