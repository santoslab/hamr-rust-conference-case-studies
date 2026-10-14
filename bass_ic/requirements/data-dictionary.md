# BASS Isolate-Ethernet-Simple Data Dictionary

One entry per named data item flowing between components or across the system
boundary. Traces to `requirements/requirements.md` (Data Requirements) and
`requirements/conops.md` Appendix A (DM-003, DM-004). Reverse-engineered
(2026-07-25) from the data-type definitions in `sysml/SW.sysml`.

**Revision (CR-01).** `[Revision, CR-01, 2026-07-26 — see
action-requests/CR-01-add-RTL-mode/]` Added the `system mode` and
`attack status` data items and the four mode/attack-status flows (`c5`–`c8`);
noted the TX geofence read of `rawMessage` byte 0.

## Data Items

| Name | Type | Units | Valid Range | Description | Produced By | Consumed By |
|------|------|-------|-------------|--------------|-------------|-------------|
| ethernet frame | `SW::StructuredEthernetMessage_i` (struct) | — | see field rows + invariant below | The sole payload type on every port: a raw 1600-byte payload plus pre-decoded classification attributes | Driver, FirewallRx, ArduPilot, FirewallTx | FirewallRx, ArduPilot, FirewallTx, Driver |
| `malformedFrame` | `Base_Types::Boolean` | — | true / false | Whether the frame is malformed; firewalls drop malformed frames | frame field (pre-decoded) | FirewallRx, FirewallTx |
| `internetProtocol` | `SW::InternetProtocol` (enum) | — | `IPV4`, `IPV6` | The frame's internet-protocol classification | frame field (pre-decoded) | FirewallRx, FirewallTx |
| `frameProtocol` | `SW::FrameProtocol` (enum) | — | `TCP`, `ARP` | The frame's protocol classification | frame field (pre-decoded) | FirewallRx, FirewallTx |
| `portIsWhitelisted` | `Base_Types::Boolean` | — | true / false | Whether the frame's port is on the (abstracted) port whitelist; consulted only by FirewallRx | frame field (pre-decoded) | FirewallRx |
| `arpType` | `SW::ARP_Type` (enum) | — | `REQUEST`, `REPLY`, `NA` | The ARP message type; `NA` for non-ARP frames (see invariant) | frame field (pre-decoded) | (available to both firewalls; not tested by any current policy rule) |
| `rawMessage` | `SW::RawEthernetMessage` = fixed array of `Base_Types::Unsigned_8` | bytes | 1600 elements, each `[0,255]` | The raw ethernet frame payload; carried opaquely — never parsed, with one CR-01 exception: FirewallTx reads byte 0 as the mocked geofence-violation indicator (0 = violation) | frame field | FirewallTx (byte 0 only; otherwise carried through unchanged) |
| system mode *(CR-01)* | `SW::Mode` (enum) | — | `Init`, `Normal`, `RTL` | The system's cyber mode, broadcast by ModeManager; starts `Init`, `Normal` from the 10th ModeManager activation, `RTL` (absorbing) on attack detection | ModeManager | FirewallRx, FirewallTx |
| attack status *(CR-01)* | `SW::AttackStatus` (enum) | — | `OK`, `Attack` | A firewall's report of (mocked) attack evidence: RX — cumulative malformed count > 5 (latched by construction); TX — current frame's `rawMessage[0] == 0` (per-dispatch) | FirewallRx, FirewallTx | ModeManager |

## Frame Flows (system connections in `SW.sysml`)

| Connection | From | To | Content |
|------------|------|----|---------|
| `c1` (inbound) | Driver `EthernetFramesRx` | FirewallRx `EthernetFramesRxIn` | every frame received from the network *(mocked source)* |
| `c2` (inbound) | FirewallRx `EthernetFramesRxOut` | ArduPilot `EthernetFramesRx` | only well-formed, whitelisted IPv4/TCP frames, unchanged |
| `c3` (outbound) | ArduPilot `EthernetFramesTx` | FirewallTx `EthernetFramesTxIn` | every frame emitted by the autopilot *(mocked source)* |
| `c4` (outbound) | FirewallTx `EthernetFramesTxOut` | Driver `EthernetFramesTx` | only well-formed ARP or IPv4 frames, unchanged *(CR-01: and only in Normal mode)* |
| `c5` (attack status, CR-01) | FirewallRx `AttackStatusRx` | ModeManager `AttackStatusRx` | RX attack report (`OK`/`Attack`), sampled |
| `c6` (attack status, CR-01) | FirewallTx `AttackStatusTx` | ModeManager `AttackStatusTx` | TX attack report (`OK`/`Attack`), sampled |
| `c7` (mode, CR-01) | ModeManager `CurrentMode` | FirewallRx `CurrentMode` | current system mode, sampled |
| `c8` (mode, CR-01) | ModeManager `CurrentMode` | FirewallTx `CurrentMode` | current system mode, sampled (fan-out of the same output as `c7`) |

The frame ports (`c1`–`c4`) are EventDataPorts of
`StructuredEthernetMessage_i`; on a given dispatch a port carries either one
frame or nothing. *(CR-01)* The mode and attack-status ports (`c5`–`c8`) are
**DataPorts** (RD-4, `hamr-sysml-patterns.md` §1): a continuously-valid sampled
value is always present after initialization (initial values: mode `Init`,
attack status `OK`), and `c1`/`c2` frame delivery additionally requires Normal
mode (mode gates, CR-01). Note the sampled feedback cycle firewalls →
ModeManager → firewalls; each written mode/attack value is sampled exactly once
by its consumer under the static schedule, with latency 0 or 1 major frame
depending on domain order.

**Invariant** (`relateFrameProtocolToArpType`, data invariant on
`StructuredEthernetMessage_i`): `frameProtocol == TCP` ⇒ `arpType == NA`;
`frameProtocol == ARP` ⇒ `arpType ∈ {REQUEST, REPLY}`.

No other data items cross a component or system boundary. Classification
attributes are pre-decoded and trusted — no component derives them from
`rawMessage` (`conops.md` §9 Assumptions 1–2), the one CR-01 exception being
FirewallTx's read of `rawMessage` byte 0 as the mocked geofence indicator — and
the port whitelist itself is abstracted into the `portIsWhitelisted` boolean
rather than modeled as data.
