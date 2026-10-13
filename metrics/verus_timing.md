# Verus verification time per crate

Verus 0.2026.09.06.8dea4a2; Apple M3 Max (Mac15,8), 16 cores, macOS 26.5.1; idle CPU temperature 44.6 C. Each table is followed by a collapsible key defining its columns.

| Case study | Crate | Role | Verified | Errors | Verus total (ms) | SMT CPU time (ms) | Runs | CV total | CV SMT | Throttled runs |
|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| BASS | `ArduPilot_ArduPilot` | component | 9 | 0 | 216 | 1 | 5 | 0.6% | 0.0% | 0 |
| BASS | `FirewallRx_FirewallRx` | component | 12 | 0 | 264 | 9 | 5 | 0.7% | 4.9% | 0 |
| BASS | `data` | library | 13 | 0 | 224 | 0 | 5 | 0.5% | 0.0% | 0 |
| BASS | `GumboLib` | library | 0 | 0 | 184 | 0 | 5 | 1.0% | 0.0% | 0 |
| BASS | `FirewallTx_FirewallTx` | component | 12 | 0 | 255 | 8 | 5 | 1.1% | 0.0% | 0 |
| BASS | `LowLevelEthernetDriver_LowLevelEthernetDriver` | component | 9 | 0 | 217 | 1 | 5 | 0.7% | 0.0% | 0 |
| BASS | `ModeManager_ModeManager` | component | 11 | 0 | 241 | 4 | 5 | 0.8% | 0.0% | 0 |
| Open Platform | `seL4_LowLevelEthernetDriver_LowLevelEthernetDriver` | component | 18 | 0 | 281 | 4 | 5 | 0.3% | 0.0% | 0 |
| Open Platform | `seL4_MavlinkFirewall_MavlinkFirewall` | component | 26 | 0 | 692 | 123 | 5 | 1.2% | 0.4% | 0 |
| Open Platform | `mavlink_parser_vest` | library | 216 | 0 | 2521 | 1628 | 5 | 0.3% | 0.3% | 0 |
| Open Platform | `vest_lib` | library | 3177 | 0 | 20590 | 39105 | 5 | 0.2% | 0.3% | 0 |
| Open Platform | `seL4_RxFirewall_RxFirewall` | component | 40 | 0 | 4433 | 4031 | 5 | 0.4% | 0.5% | 0 |
| Open Platform | `data` | library | 8 | 0 | 219 | 0 | 5 | 0.6% | 0.0% | 0 |
| Open Platform | `GumboLib` | library | 0 | 0 | 230 | 0 | 5 | 0.5% | 0.0% | 0 |
| Open Platform | `firewall-core` | library | 39 | 0 | 579 | 291 | 5 | 0.7% | 0.8% | 0 |
| Open Platform | `seL4_TxFirewall_TxFirewall` | component | 20 | 0 | 974 | 650 | 5 | 0.7% | 0.6% | 0 |
| Isolette | `operator_interface_oip_oit` | component | 22 | 0 | 265 | 12 | 5 | 0.4% | 0.0% | 0 |
| Isolette | `sys_nominal_proof` | component | 1862 | 0 | 1954 | 1461 | 5 | 0.2% | 0.6% | 0 |
| Isolette | `test_controller` | component | 2 | 0 | 252 | 0 | 5 | 1.1% | 0.0% | 0 |
| Isolette | `data` | library | 20 | 0 | 218 | 0 | 5 | 0.5% | 0.0% | 0 |
| Isolette | `GUMBO_Library` | library | 0 | 0 | 182 | 0 | 5 | 0.8% | 0.0% | 0 |
| Isolette | `observers` | library | 18 | 0 | 262 | 0 | 5 | 0.3% | 0.0% | 0 |
| Isolette | `thermostat_mt_dmf_dmf` | component | 7 | 0 | 200 | 0 | 5 | 0.6% | 0.0% | 0 |
| Isolette | `thermostat_mt_ma_ma` | component | 15 | 0 | 260 | 6 | 5 | 0.8% | 8.6% | 0 |
| Isolette | `thermostat_mt_mmi_mmi` | component | 18 | 0 | 285 | 17 | 5 | 1.3% | 2.6% | 0 |
| Isolette | `thermostat_mt_mmm_mmm` | component | 14 | 0 | 250 | 5 | 5 | 0.8% | 9.3% | 0 |
| Isolette | `thermostat_rt_drf_drf` | component | 7 | 0 | 201 | 0 | 5 | 1.0% | 0.0% | 0 |
| Isolette | `thermostat_rt_mhs_mhs` | component | 15 | 0 | 252 | 4 | 5 | 0.4% | 10.6% | 0 |
| Isolette | `thermostat_rt_mri_mri` | component | 19 | 0 | 298 | 24 | 5 | 0.2% | 2.3% | 0 |
| Isolette | `thermostat_rt_mrm_mrm` | component | 14 | 0 | 244 | 4 | 5 | 2.1% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic` | component | 15 | 0 | 231 | 2 | 5 | 0.4% | 0.0% | 0 |
| RTS | `data` | library | 0 | 0 | 154 | 0 | 5 | 0.7% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic` | component | 15 | 0 | 232 | 2 | 5 | 0.2% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic` | component | 11 | 0 | 215 | 1 | 5 | 0.3% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic` | component | 15 | 0 | 232 | 2 | 5 | 0.5% | 20.3% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic` | component | 15 | 0 | 231 | 2 | 5 | 0.9% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic` | component | 15 | 0 | 235 | 3 | 5 | 2.1% | 21.1% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic` | component | 11 | 0 | 214 | 1 | 5 | 0.4% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic` | component | 15 | 0 | 233 | 2 | 5 | 1.4% | 20.3% | 0 |
| RTS | `actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic` | component | 11 | 0 | 215 | 1 | 5 | 1.6% | 0.0% | 0 |
| RTS | `actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator` | component | 11 | 0 | 216 | 1 | 5 | 2.0% | 0.0% | 0 |
| RTS | `actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic` | component | 11 | 0 | 215 | 1 | 5 | 1.2% | 0.0% | 0 |
| RTS | `actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator` | component | 11 | 0 | 217 | 1 | 5 | 1.0% | 0.0% | 0 |
| RTS | `actuatorsMock_actuatorsMockThread` | component | 10 | 0 | 207 | 0 | 5 | 0.5% | 0.0% | 0 |
| RTS | `eventControlMock_eventControlMockThread` | component | 10 | 0 | 217 | 2 | 5 | 0.7% | 0.0% | 0 |
| RTS | `instrumentationMock_instrumentationMockThread` | component | 33 | 0 | 544 | 69 | 5 | 0.4% | 0.8% | 0 |

<details>
<summary>Key</summary>

Columns, left to right:

- **Case study**: the system.
- **Crate**: the Cargo package name.
- **Role**: *component* = a crate verified through its own `make verus` target (the thread crates, and Isolette's test controller and system-proof crate); *library* = a library crate (`data`, the GUMBO library crate, `firewall-core`, `observers`, `mavlink_parser_vest`, and the third-party `vest_lib`), measured while verifying one crate that depends on it.
- **Verified**: number of functions Verus verified in the crate (its `verification results:: N verified`).
- **Errors**: number of verification errors.
- **Verus total (ms)**: median over the runs of Verus' reported `total-time` for the crate: parsing, type checking, VIR generation, SMT solving and lifetime checking. Cargo's compilation of dependencies is not included.
- **SMT CPU time (ms)**: median of the time Z3 spent discharging the crate's verification conditions (Verus' `total smt-run`), *summed over Verus' parallel solver threads* (up to 15 here). It is CPU time, not elapsed time, so it can exceed Verus total (e.g. `vest_lib`).
- **Runs**: number of measured runs.
- **CV total / CV SMT**: coefficient of variation (standard deviation / mean) of Verus total and SMT CPU time over the runs. Verus reports times in whole milliseconds, so for SMT times of a few milliseconds a large CV is rounding, not variability.
- **Throttled runs**: runs before or after which macOS reported a thermal state other than nominal (`ProcessInfo.thermalState`). Per-run CPU temperature, fan speed and peak P-cluster frequency (from `macmon`, sampled every 100 ms) are in `verus_timing.csv`.

**Method.** Every crate was first verified once (vstd and dependencies verified and cached; one shared Cargo target directory per case study; case studies warmed up in parallel), followed by a cool-down of at least 180 s until the CPU was within 3 C of its idle temperature, the thermal state nominal and the fans stopped. Then 5 rounds, each re-verifying every crate once in turn: only the crate's own Cargo fingerprint (and, for a library, the library's) is removed and `make verus` (`make all` for the system-proof crate) is rerun with Verus' `--time`. Each measured run is preceded by a cool-down of at least 5 s until the CPU is within 5 C of idle and the thermal state nominal. Cargo runs one job at a time (`CARGO_BUILD_JOBS=1`); Verus itself uses all its threads.

**Settings.** The generated Makefiles' `SMT_OPTS` (`--rlimit 100 --smt-option smt.random_seed=7`). Exceptions: the RTS instrumentation mock also uses `CARGO_VERUS_OPTS="--fwd-verus-args-to roots"` and `--smt-option smt.relevancy=0` (see `rts/readme.md`); Open Platform's ethernet driver is verified with `MICROKIT_BOARD=qemu_virt_aarch64`.

</details>

## Variability and number of runs

0 measured run(s) were flagged as possibly throttled.
No crate with a median of at least 100 ms has a coefficient of variation above 5% (largest: `thermostat_rt_mrm_mrm` 2.1%, `actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic` 2.1%, `actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator` 2.0%). **Recommendation:** 5 runs are sufficient; more runs would not change the medians materially.

<details>
<summary>Key</summary>

- **Median total (ms)**: median Verus total time of the crate.
- **CV total**: coefficient of variation of its Verus total time.
- **Runs for +-5% (95% CI)**: runs needed for the 95% confidence interval of the mean Verus total time to be within +-5% of the mean, assuming normally distributed times: ceil((1.96 * CV / 0.05)^2).

</details>

