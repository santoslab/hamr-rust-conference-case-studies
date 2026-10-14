# Architecture and GUMBO contract metrics (from HAMR codegen reports)

Counted from HAMR's codegen reports (see `README.md` for how they were produced). Each table is followed by a collapsible key defining its columns.

## Per case study (all thread instances)

| Case study | Threads (types) | Ports in/out | state vars | functions | invariants | integ. assume | integ. guarantee | init guarantee | compute assume | compute guarantee | compute case | handler | Clauses | Verus lines |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| BASS | 5 (5) | 8/7 | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 22 | 0 | 0 | 25 | 131 |
| Open Platform | 5 (5) | 24/24 | 0 | 3 | 0 | 0 | 4 | 0 | 0 | 52 | 0 | 0 | 56 | 256 |
| Isolette | 11 (11) | 28/21 | 5 | 8 | 0 | 2 | 2 | 8 | 6 | 5 | 36 | 0 | 59 | 373 |
| RTS | 15 (6) | 38/38 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 12 | 0 | 0 | 14 | 98 |
| ICS | 12 (12) | 23/21 | 9 | 2 | 0 | 0 | 0 | 5 | 3 | 19 | 0 | 0 | 27 | 83 |

<details>
<summary>Key</summary>

Columns, left to right:

- **Case study**: the system.
- **Threads (types)**: number of thread instances in the system; in parentheses, the number of distinct thread definitions they instantiate.
- **Ports in/out**: total number of input / output ports (data, event and event-data) over all thread instances.
- **state vars**: GUMBO `state` variable declarations.
- **functions**: GUMBO functions (`def` / `@spec def`) declared in the thread's own GUMBO block (functions of GUMBO library packages are not included; see `sysml_loc.md`).
- **invariants**: GUMBO `invariants` clauses.
- **integ. assume**: `integration` `assume` clauses (constraints on values arriving on input ports).
- **integ. guarantee**: `integration` `guarantee` clauses (constraints on values sent on output ports).
- **init guarantee**: `initialize` `guarantee` clauses.
- **compute assume**: `compute` `assume` clauses (general preconditions of the compute entry point).
- **compute guarantee**: `compute` `guarantee` clauses (general postconditions).
- **compute case**: `compute` `case` clauses (each an assume / guarantee pair).
- **handler**: event-port `handle` clauses (sporadic threads).
- **Clauses**: sum of invariants, integ. assume, integ. guarantee, init guarantee, compute assume, compute guarantee, compute case and handler (state vars and functions are declarations, not clauses).
- **Verus lines**: number of source lines of the Verus code HAMR generated for those clauses (each clause's position in the generated Rust as recorded in the report, end line - begin line + 1; measured in the macro-syntax build the report came from, see `README.md`).

Every count is summed over all thread *instances*: the contract of a thread definition that is instantiated several times (RTS) is counted once per instance. The reports list threads only (not processes or systems).

</details>


## Per thread type


### BASS

| Thread type | Instances | Ports in/out | state vars | functions | invariants | integ. assume | integ. guarantee | init guarantee | compute assume | compute guarantee | compute case | handler | Clauses | Verus lines |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `SW::ArduPilot_i` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `SW::Firewall_Rx_i` | 1 | 2/2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 9 | 0 | 0 | 10 | 54 |
| `SW::Firewall_Tx_i` | 1 | 2/2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 6 | 0 | 0 | 7 | 37 |
| `SW::LowLevelEthernetDriver_i` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `SW::ModeManager_i` | 1 | 2/1 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 7 | 0 | 0 | 8 | 40 |

### Open Platform

| Thread type | Instances | Ports in/out | state vars | functions | invariants | integ. assume | integ. guarantee | init guarantee | compute assume | compute guarantee | compute case | handler | Clauses | Verus lines |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `SW::MavlinkFirewall` | 1 | 4/4 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 16 | 68 |
| `SW::RxFirewall` | 1 | 4/8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 20 | 96 |
| `SW::TxFirewall` | 1 | 4/4 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 16 | 0 | 0 | 20 | 92 |
| `SW::LowLevelEthernetDriver` | 1 | 4/4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `SW::ArduPilot` | 1 | 8/4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Isolette

| Thread type | Instances | Ports in/out | state vars | functions | invariants | integ. assume | integ. guarantee | init guarantee | compute assume | compute guarantee | compute case | handler | Clauses | Verus lines |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `Regulate::Manage_Regulator_Interface_i` | 1 | 4/5 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 9 | 0 | 12 | 69 |
| `Regulate::Manage_Heat_Source_i` | 1 | 4/1 | 1 | 0 | 0 | 0 | 0 | 2 | 1 | 1 | 5 | 0 | 9 | 48 |
| `Regulate::Manage_Regulator_Mode_i` | 1 | 3/1 | 1 | 2 | 0 | 0 | 0 | 1 | 0 | 1 | 5 | 0 | 7 | 52 |
| `Regulate::Detect_Regulator_Failure_i` | 1 | 0/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `Monitor::Manage_Monitor_Interface_i` | 1 | 4/4 | 1 | 1 | 0 | 2 | 0 | 1 | 1 | 0 | 7 | 0 | 11 | 58 |
| `Monitor::Manage_Alarm_i` | 1 | 4/1 | 1 | 1 | 0 | 0 | 0 | 1 | 3 | 0 | 5 | 0 | 9 | 71 |
| `Monitor::Manage_Monitor_Mode_i` | 1 | 3/1 | 1 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 5 | 0 | 7 | 56 |
| `Monitor::Detect_Monitor_Failure_i` | 1 | 0/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `Operator_Interface::Operator_Interface_Thread_i` | 1 | 4/4 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 2 | 0 | 0 | 4 | 19 |
| `Devices::Temperature_Sensor_i` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `Devices::Heat_Source_i` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### RTS

| Thread type | Instances | Ports in/out | state vars | functions | invariants | integ. assume | integ. guarantee | init guarantee | compute assume | compute guarantee | compute case | handler | Clauses | Verus lines |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `Instrumentation::InstrumentationMockThread_i` | 1 | 0/24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `EventControl::EventControlMockThread_i` | 1 | 0/2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `Actuators::ActuatorsMockThread_i` | 1 | 2/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `Actuation::CoincidenceLogic_i` | 6 | 4/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 13 |
| `Actuation::OrLogic_i` | 4 | 2/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 2 |
| `Actuation::Actuator_i` | 2 | 2/1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 2 | 6 |

### ICS

| Thread type | Instances | Ports in/out | state vars | functions | invariants | integ. assume | integ. guarantee | init guarantee | compute assume | compute guarantee | compute case | handler | Clauses | Verus lines |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `GroundStation::WifiDriver_t` | 1 | 3/3 | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 2 | 0 | 0 | 5 | 14 |
| `GroundStation::WifiDriverVM_t` | 1 | 2/2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `GroundStation::BtDriver_t` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `GroundStation::UsbDriver_t` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `GroundStation::DataManager_t` | 1 | 4/3 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 3 | 9 |
| `GroundStation::DataStorage_t` | 1 | 3/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `GroundStation::DataAnalysis_t` | 1 | 2/2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 3 |
| `GroundStation::Decryptor_t` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 3 |
| `GroundStation::Encryptor_t` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 2 | 6 |
| `GroundStation::LogMonitor_t` | 1 | 2/3 | 3 | 0 | 0 | 0 | 0 | 2 | 0 | 5 | 0 | 0 | 7 | 24 |
| `GroundStation::ReportMonitor_t` | 1 | 2/2 | 4 | 1 | 0 | 0 | 0 | 1 | 0 | 6 | 0 | 0 | 7 | 21 |
| `GroundStation::Firewall_t` | 1 | 1/1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 3 |

<details>
<summary>Key</summary>

Columns, left to right:

- **Thread type**: a distinct thread definition (`<package>::<part def>`).
- **Instances**: how many thread instances in the system use it.
- **Ports in/out**: number of input / output ports of one instance.
- **state vars**: GUMBO `state` variable declarations.
- **functions**: GUMBO functions (`def` / `@spec def`) declared in the thread's own GUMBO block (functions of GUMBO library packages are not included; see `sysml_loc.md`).
- **invariants**: GUMBO `invariants` clauses.
- **integ. assume**: `integration` `assume` clauses (constraints on values arriving on input ports).
- **integ. guarantee**: `integration` `guarantee` clauses (constraints on values sent on output ports).
- **init guarantee**: `initialize` `guarantee` clauses.
- **compute assume**: `compute` `assume` clauses (general preconditions of the compute entry point).
- **compute guarantee**: `compute` `guarantee` clauses (general postconditions).
- **compute case**: `compute` `case` clauses (each an assume / guarantee pair).
- **handler**: event-port `handle` clauses (sporadic threads).
- **Clauses**: sum of invariants, integ. assume, integ. guarantee, init guarantee, compute assume, compute guarantee, compute case and handler (state vars and functions are declarations, not clauses).
- **Verus lines**: number of source lines of the Verus code HAMR generated for those clauses (each clause's position in the generated Rust as recorded in the report, end line - begin line + 1; measured in the macro-syntax build the report came from, see `README.md`).

One row per thread definition; all columns after Instances are for a single instance (instances of a definition share its ports and contract).

</details>

