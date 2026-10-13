# BASS Isolate-Ethernet-Simple — Component Requirements

This document decomposes the system-level requirements from `requirements.md` into
component-level requirements for the LowLevelEthernetDriver, RX Firewall
(`FirewallRx`), ArduPilot, TX Firewall (`FirewallTx`), and Mode Manager
(`ModeManager`) components.

**Revision (CR-01).** `[Revision, CR-01, 2026-07-26 — see
action-requests/CR-01-add-RTL-mode/]` Added the ModeManager section, made both
firewall sections mode-aware (mode-gate + detection rows; pass rows re-scoped
to Normal mode), and extended the GUMBO-label mapping with the `CR01_*`
guarantee labels. Drop and no-input rows remain unconditional (they hold in
every mode — see `requirements.md`, Revision note). Requirements
are written in structured natural language to facilitate mapping to GUMBO formal
specifications — here in reverse: the firewall rows below were **reverse-engineered
(2026-07-25)** from the GUMBO compute contracts already present in
`sysml/SW.sysml`, and each row's *GUMBO Label (Source HLR)* column names the
guarantee it restates, with the full-system HLR ID from that guarantee's docstring
in brackets. The corresponding unit/GUMBOX tests in
`hamr/microkit/crates/<component>/src/test/tests.rs` are keyed to the same HLR
numbers (FirewallRx: `test_RC_INSPECTA_00_HLR_9_...`; FirewallTx uses the variant
prefix `test_compute_REQ_INSPECTA_HLR_12_...`).

## Glossary

| Term | Definition |
|------|-----------|
| **frame** | An `SW::StructuredEthernetMessage_i`: a fixed 1600-byte raw payload plus pre-decoded classification attributes |
| **well-formed / malformed** | The frame's `malformedFrame` attribute is false / true |
| **IPv4 / IPv6 frame** | The frame's `internetProtocol` attribute is `IPV4` / `IPV6` |
| **TCP / ARP frame** | The frame's `frameProtocol` attribute is `TCP` / `ARP` |
| **whitelisted** | The frame's `portIsWhitelisted` attribute is true (the port whitelist itself is abstracted to this boolean) |
| **ARP type** | The frame's `arpType` attribute (`REQUEST`, `REPLY`, or `NA`); constrained by the frame invariant (TCP ⇒ `NA`, ARP ⇒ `REQUEST`/`REPLY`) |
| **pass (copy through)** | Emit the received frame on the output port unchanged (`MustSend`, output == input) |
| **drop** | Emit nothing on the output port for the received frame (`NoSend`) |
| **Driver** | Shorthand for `LowLevelEthernetDriver` |
| **mode** *(CR-01)* | The value of `SW::Mode` (`Init`, `Normal`, `RTL`) sampled on a component's `CurrentMode` DataPort input, or held/broadcast by the ModeManager |
| **attack status** *(CR-01)* | A value of `SW::AttackStatus` (`OK`, `Attack`) on a firewall's attack-status DataPort output |
| **malformed count** *(CR-01)* | FirewallRx's cumulative count of malformed received frames since initialization, saturating at 6 (RD-1) |
| **geofence indicator** *(CR-01)* | Byte 0 of a frame's `rawMessage` equal to 0 — the mocked geofence-violation evidence (RD-2) |

## LowLevelEthernetDriver Component Requirements *(mocked)*

The Driver is the system's boundary to the physical network interface. It is
**mocked**: it carries no GUMBO contract and its current implementation is a no-op
stub with no port I/O. The requirements below state its intended role
(`Req_Transport`) and are neither contracted nor implemented.

### Compute Requirements

| Req ID | Traces To | GUMBO Label (Source HLR) | Requirement |
|--------|-----------|--------------------------|-------------|
| **Driver_Req_RxRelay** | Req_Transport | — (mocked; no contract) | Each frame received from the physical network interface shall be placed on `EthernetFramesRx` (toward the RX Firewall) |
| **Driver_Req_TxRelay** | Req_Transport | — (mocked; no contract) | Each frame received on `EthernetFramesTx` (from the TX Firewall) shall be transmitted on the physical network interface |

## FirewallRx Component Requirements

The RX Firewall (`Firewall_Rx_i`) mediates the inbound path. Its policy is a
default-deny allow-list: **in Normal mode**, a received frame is copied through
to `ArduPilot` only if it is well-formed, IPv4, TCP, and whitelisted; every
other received frame is dropped; **in Init and RTL modes every frame is
dropped** *(CR-01)*. Independently of mode, it counts malformed received frames
and reports attack status *(CR-01)*. Requirement text follows the formal
predicates (see `requirements.md`, Reverse-Engineering Observations 2–3, for
docstring discrepancies and the label/source-HLR offset).

Ports *(CR-01 additions)*: `CurrentMode : DataPort in SW::Mode`,
`AttackStatusRx : DataPort out SW::AttackStatus`.
GUMBO state *(CR-01)*: `malformedCount` (spec-relevant per
`hamr-sysml-patterns.md` §4 — the detection requirement constrains it across
dispatches).

### Compute Requirements

| Req ID | Traces To | GUMBO Label (Source HLR) | Requirement |
|--------|-----------|--------------------------|-------------|
| **FirewallRx_Req_NoInput** | Req_Rx_NoInput | `RC_INSPECTA_00_HLR_1` [HLR-1] | When no frame is present on `EthernetFramesRxIn`, no frame shall be sent on `EthernetFramesRxOut` *(all modes)* |
| **FirewallRx_Req_Drop_Malformed** | Req_Rx_Drop_Malformed | `RC_INSPECTA_00_HLR_2` [HLR-1] | When the received frame is malformed, no frame shall be sent on `EthernetFramesRxOut` *(all modes)* |
| **FirewallRx_Req_Drop_IPv6** | Req_Rx_Drop_IPv6 | `RC_INSPECTA_00_HLR_4` [HLR-2] | When the received frame is IPv6, no frame shall be sent on `EthernetFramesRxOut` *(all modes)* |
| **FirewallRx_Req_Drop_ARP** | Req_Rx_Drop_ARP | `RC_INSPECTA_00_HLR_6` [HLR-4] | When the received frame is ARP (any ARP type, any internet protocol), no frame shall be sent on `EthernetFramesRxOut` *(all modes)* |
| **FirewallRx_Req_Drop_NonWhitelisted** | Req_Rx_Drop_NonWhitelisted | `RC_INSPECTA_00_HLR_8` [HLR-6] | When the received frame is IPv4 and TCP and not whitelisted, no frame shall be sent on `EthernetFramesRxOut` *(all modes)* |
| **FirewallRx_Req_Pass** *(revised, CR-01)* | Req_Rx_Allow | `RC_INSPECTA_00_HLR_9` [HLR-8] | When the sampled mode is `Normal` and the received frame is IPv4, TCP, whitelisted, and well-formed, that frame shall be sent unchanged on `EthernetFramesRxOut` |
| **FirewallRx_Req_ModeGate** *(new, CR-01)* | Req_Rx_ModeGate | `CR01_Rx_ModeGate` | When the sampled mode is not `Normal` (i.e., `Init` or `RTL`), no frame shall be sent on `EthernetFramesRxOut`, regardless of input |
| **FirewallRx_Req_Count** *(new, CR-01)* | Req_Detect_Rx | `CR01_Rx_Count` | `malformedCount` shall increment by 1 on each dispatch that receives a malformed frame and remain unchanged otherwise, saturating at 6 (mode-independent) |
| **FirewallRx_Req_Detect** *(new, CR-01)* | Req_Detect_Rx | `CR01_Rx_Detect` | On every dispatch, `AttackStatusRx` shall read `Attack` when `malformedCount` (post-update) exceeds 5, and `OK` otherwise |

### Initialize Requirements *(new, CR-01)*

| Req ID | Traces To | GUMBO Label | Requirement |
|--------|-----------|-------------|-------------|
| **FirewallRx_Req_Init** | Req_Detect_Rx, Req_Mode_Init | `CR01_Rx_Init` | At initialization: `malformedCount == 0` and `AttackStatusRx == OK` (DataPort output initialization obligation) |

## ArduPilot Component Requirements *(mocked)*

ArduPilot stands in for the legacy autonomy application (a VM-hosted legacy
software stack in the full system). It is **mocked**: no GUMBO contract, and the
current implementation is a no-op stub with no port I/O. The requirements below
state its intended role (`Req_Autonomy`).

### Compute Requirements

| Req ID | Traces To | GUMBO Label (Source HLR) | Requirement |
|--------|-----------|--------------------------|-------------|
| **ArduPilot_Req_Consume** | Req_Autonomy | — (mocked; no contract) | Frames delivered on `EthernetFramesRx` shall be consumed as the autonomy application's inbound traffic |
| **ArduPilot_Req_Produce** | Req_Autonomy | — (mocked; no contract) | The autonomy application's outbound traffic shall be placed on `EthernetFramesTx` (toward the TX Firewall) |

## FirewallTx Component Requirements

The TX Firewall (`Firewall_Tx_i`) mediates the outbound path. Its policy is more
permissive than the RX Firewall's — it does not consult the port whitelist, and it
passes ARP so that address-resolution traffic can leave the platform: **in
Normal mode**, a received frame is copied through only if it is well-formed and
either ARP or IPv4; a frame that is malformed, or neither IPv4 nor ARP, is
dropped; **in Init and RTL modes every frame is dropped** *(CR-01)*.
Independently of mode, it inspects each received frame's geofence indicator and
reports attack status *(CR-01)*.

Ports *(CR-01 additions)*: `CurrentMode : DataPort in SW::Mode`,
`AttackStatusTx : DataPort out SW::AttackStatus`. No GUMBO state — TX detection
is a per-dispatch pure function of the input (`requirements.md`,
`Req_Detect_Tx`).

### Compute Requirements

| Req ID | Traces To | GUMBO Label (Source HLR) | Requirement |
|--------|-----------|--------------------------|-------------|
| **FirewallTx_Req_Pass_ARP** *(revised, CR-01)* | Req_Tx_Allow_ARP | `RC_INSPECTA_00_HLR_7` [HLR-7] | When the sampled mode is `Normal` and the received frame is well-formed and ARP, that frame shall be sent unchanged on `EthernetFramesTxOut` |
| **FirewallTx_Req_Pass_IPv4** *(revised, CR-01)* | Req_Tx_Allow_IPv4 | `RC_INSPECTA_00_HLR_12` [HLR-12] | When the sampled mode is `Normal` and the received frame is well-formed and IPv4, that frame shall be sent unchanged on `EthernetFramesTxOut` |
| **FirewallTx_Req_Drop** | Req_Tx_Drop | `RC_INSPECTA_00_HLR_14` [HLR-14] | When the received frame is malformed, or is neither IPv4 nor ARP, no frame shall be sent on `EthernetFramesTxOut` *(all modes)* |
| **FirewallTx_Req_NoInput** | Req_Tx_NoInput | `RC_INSPECTA_00_HLR_16` [HLR-16] | When no frame is present on `EthernetFramesTxIn`, no frame shall be sent on `EthernetFramesTxOut` *(all modes)* |
| **FirewallTx_Req_ModeGate** *(new, CR-01)* | Req_Tx_ModeGate | `CR01_Tx_ModeGate` | When the sampled mode is not `Normal` (i.e., `Init` or `RTL`), no frame shall be sent on `EthernetFramesTxOut`, regardless of input |
| **FirewallTx_Req_Detect** *(new, CR-01)* | Req_Detect_Tx | `CR01_Tx_Detect` | On every dispatch, `AttackStatusTx` shall read `Attack` when a frame is received whose `rawMessage` byte 0 equals 0, and `OK` otherwise (including no-input dispatches); detection is mode-independent |

*(A well-formed IPv4 ARP frame satisfies both pass rules; they agree — the frame
is copied through unchanged.)*

### Initialize Requirements *(new, CR-01)*

| Req ID | Traces To | GUMBO Label | Requirement |
|--------|-----------|-------------|-------------|
| **FirewallTx_Req_Init** | Req_Detect_Tx | `CR01_Tx_Init` | At initialization: `AttackStatusTx == OK` (DataPort output initialization obligation) |

## ModeManager Component Requirements *(new, CR-01)*

The Mode Manager (`ModeManager_i`, scheduling domain 6) is the system's mode
authority: it consumes both firewalls' attack-status feeds (sampled DataPorts)
and broadcasts the current system mode on its `CurrentMode` DataPort output.
Mode semantics: start in `Init`; transition to `Normal` at the 10th activation;
transition to `RTL` when either attack feed reads `Attack` (from Init or
Normal, with RTL winning ties against the Init→Normal transition); `RTL` is
absorbing until restart (RD-3).

Ports: `AttackStatusRx : DataPort in SW::AttackStatus`,
`AttackStatusTx : DataPort in SW::AttackStatus`,
`CurrentMode : DataPort out SW::Mode`.
GUMBO state: `currentMode : SW::Mode`, `activationCount :
Base_Types::Integer_32` (both spec-relevant per `hamr-sysml-patterns.md` §4 —
the mode-machine requirements constrain them across dispatches).

### Initialize Requirements

| Req ID | Traces To | GUMBO Label | Requirement |
|--------|-----------|-------------|-------------|
| **ModeManager_Req_Init** | Req_Mode_Init | `CR01_MM_Init` | At initialization: `currentMode == Init`, `activationCount == 0`, and the `CurrentMode` output port reads `Init` (DataPort output initialization obligation) |

### Compute Requirements

| Req ID | Traces To | GUMBO Label | Requirement |
|--------|-----------|-------------|-------------|
| **ModeManager_Req_Count** | Req_Mode_Normal | `CR01_MM_Count` | `activationCount` shall increment by 1 each dispatch, saturating at 10 |
| **ModeManager_Req_ToRTL** | Req_Mode_RTL | `CR01_MM_ToRTL` | When the previous mode is not `RTL` and either attack-status input reads `Attack`, `currentMode` shall become `RTL` |
| **ModeManager_Req_StayInit** | Req_Mode_Normal | `CR01_MM_StayInit` | When the previous mode is `Init`, neither attack-status input reads `Attack`, and the post-increment `activationCount` is below 10, `currentMode` shall remain `Init` |
| **ModeManager_Req_ToNormal** | Req_Mode_Normal | `CR01_MM_ToNormal` | When the previous mode is `Init`, neither attack-status input reads `Attack`, and the post-increment `activationCount` reaches 10, `currentMode` shall become `Normal` |
| **ModeManager_Req_StayNormal** | Req_Mode_Normal | `CR01_MM_StayNormal` | When the previous mode is `Normal` and neither attack-status input reads `Attack`, `currentMode` shall remain `Normal` |
| **ModeManager_Req_Absorbing** | Req_Mode_Absorbing | `CR01_MM_Absorbing` | When the previous mode is `RTL`, `currentMode` shall remain `RTL` |
| **ModeManager_Req_Broadcast** | Req_Mode_Broadcast | `CR01_MM_Broadcast` | On every dispatch, the `CurrentMode` output shall equal the (post-transition) `currentMode` state |

## Integration Requirements (all components)

The model defines **no port-level GUMBO `integration` constraints** — neither
firewall assumes anything about incoming frame values, and neither guarantees a
value property on its output port beyond what the compute contracts state.
*(Re-recorded for CR-01, 2026-07-26: the new mode / attack-status ports also
carry no integration constraints — their enum payloads have no invalid values
to exclude, and per `hamr-sysml-patterns.md` §2 the reusable-component style
keeps context facts out of per-port invariants.)* The only model-level value
constraint is the data-type invariant:

| Req ID | Traces To | GUMBO Label (Source HLR) | Requirement |
|--------|-----------|--------------------------|-------------|
| **Frame_Inv_ArpType** | Data Requirements (`requirements.md`) | `relateFrameProtocolToArpType` (data invariant on `StructuredEthernetMessage_i`) | Every frame shall satisfy: TCP ⇒ `arpType == NA`; ARP ⇒ `arpType ∈ {REQUEST, REPLY}` |

Consequence (recorded per `hamr-sysml-patterns.md` §2): with zero receiver-side
integration assumes, a `SysGUMBOIntegrationCheck` run on this model generates zero
verification conditions and passes **vacuously**; the system currently has no
machine-checked cross-component argument. The security policy is carried entirely
by the two firewalls' compute contracts, checked per-component by Verus and the
GUMBOX test harnesses.

## Timing Requirements (all components)

| Req ID | Traces To | Requirement |
|--------|-----------|-------------|
| **Timing_Req_Period** *(revised, CR-01)* | Req_Timing | Driver, FirewallRx, FirewallTx, ArduPilot, and ModeManager shall each be dispatched periodically with a period of 1000 ms (declared compute execution time 100 ms each) |
| **Timing_Req_Isolation** *(revised, CR-01)* | Req_Isolation | Each component shall run in its own seL4 protection domain (one thread per process; scheduling domains 2–6 under the 1000 ms static cyclic major frame) |

## Traceability Summary

| System Requirement | Driver | FirewallRx | ArduPilot | FirewallTx | ModeManager |
|--------------------|--------|------------|-----------|------------|-------------|
| Req_Rx_Allow | — | FirewallRx_Req_Pass | — | — | — |
| Req_Rx_Drop_Malformed | — | FirewallRx_Req_Drop_Malformed | — | — | — |
| Req_Rx_Drop_IPv6 | — | FirewallRx_Req_Drop_IPv6 | — | — | — |
| Req_Rx_Drop_ARP | — | FirewallRx_Req_Drop_ARP | — | — | — |
| Req_Rx_Drop_NonWhitelisted | — | FirewallRx_Req_Drop_NonWhitelisted | — | — | — |
| Req_Rx_NoInput | — | FirewallRx_Req_NoInput | — | — | — |
| Req_Rx_ModeGate *(CR-01)* | — | FirewallRx_Req_ModeGate | — | — | — |
| Req_Tx_Allow_ARP | — | — | — | FirewallTx_Req_Pass_ARP | — |
| Req_Tx_Allow_IPv4 | — | — | — | FirewallTx_Req_Pass_IPv4 | — |
| Req_Tx_Drop | — | — | — | FirewallTx_Req_Drop | — |
| Req_Tx_NoInput | — | — | — | FirewallTx_Req_NoInput | — |
| Req_Tx_ModeGate *(CR-01)* | — | — | — | FirewallTx_Req_ModeGate | — |
| Req_Detect_Rx *(CR-01)* | — | FirewallRx_Req_Count, FirewallRx_Req_Detect, FirewallRx_Req_Init | — | — | — |
| Req_Detect_Tx *(CR-01)* | — | — | — | FirewallTx_Req_Detect, FirewallTx_Req_Init | — |
| Req_Mode_Init *(CR-01)* | — | — | — | — | ModeManager_Req_Init |
| Req_Mode_Normal *(CR-01)* | — | — | — | — | ModeManager_Req_Count, ModeManager_Req_StayInit, ModeManager_Req_ToNormal, ModeManager_Req_StayNormal |
| Req_Mode_RTL *(CR-01)* | — | — | — | — | ModeManager_Req_ToRTL |
| Req_Mode_Absorbing *(CR-01)* | — | — | — | — | ModeManager_Req_Absorbing |
| Req_Mode_Broadcast *(CR-01)* | — | — | — | — | ModeManager_Req_Broadcast |
| Req_Transport *(mocked)* | Driver_Req_RxRelay, Driver_Req_TxRelay | — | — | — | — |
| Req_Autonomy *(mocked)* | — | — | ArduPilot_Req_Consume, ArduPilot_Req_Produce | — | — |
| Req_Timing | Timing_Req_Period | Timing_Req_Period | Timing_Req_Period | Timing_Req_Period | Timing_Req_Period |
| Req_Isolation | Timing_Req_Isolation | Timing_Req_Isolation | Timing_Req_Isolation | Timing_Req_Isolation | Timing_Req_Isolation |

**Mediation invariant:** FirewallRx_Req_Pass and the four FirewallRx drop
requirements together mean the only frames that can reach ArduPilot are
well-formed, whitelisted IPv4/TCP frames, unchanged; FirewallTx_Req_Pass_ARP/IPv4
and FirewallTx_Req_Drop together mean the only frames that can leave the platform
are well-formed ARP or IPv4 frames, unchanged. *(CR-01 strengthens this: the
mode gates mean frames flow at all only in Normal mode — in Init and RTL,
nothing crosses either firewall in either direction.)* The asymmetry (strict default-deny
inbound, whitelist-free but protocol-restricted outbound) is deliberate: the
strictest control sits in front of the vulnerable legacy component. Because these
properties are stated only as per-component compute contracts (no integration
constraints, no system-level GUMBO specifications), the end-to-end claim rests on
the topology in `SW.sysml` — every path between the network and ArduPilot passes
through exactly one firewall — plus the seL4 isolation recorded in
Timing_Req_Isolation.
