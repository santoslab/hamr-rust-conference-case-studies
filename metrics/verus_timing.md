# Verus verification time per crate

Verus 0.2026.09.06.8dea4a2; Apple M3 Max (Mac15,8), 16 cores, macOS 26.5.1; idle CPU temperature 44.6 C. Each table is followed by a collapsible key defining its columns.

| Case study | Crate | Role | Verified | Errors | Verus total (ms) | SMT CPU time (ms) | Runs | CV total | CV SMT | Throttled runs |
|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| BASS | `ArduPilot_ArduPilot` | component | 9 | 0 | 217 | 1 | 5 | 0.8% | 0.0% | 0 |
| BASS | `FirewallRx_FirewallRx` | component | 12 | 0 | 263 | 9 | 5 | 2.5% | 5.8% | 0 |
| BASS | `data` | library | 13 | 0 | 224 | 0 | 5 | 0.7% | 0.0% | 0 |
| BASS | `GumboLib` | library | 0 | 0 | 185 | 0 | 5 | 1.6% | 0.0% | 0 |
| BASS | `FirewallTx_FirewallTx` | component | 12 | 0 | 255 | 8 | 5 | 1.1% | 5.5% | 0 |
| BASS | `LowLevelEthernetDriver_LowLevelEthernetDriver` | component | 9 | 0 | 218 | 1 | 5 | 0.8% | 0.0% | 0 |
| BASS | `ModeManager_ModeManager` | component | 11 | 0 | 241 | 4 | 5 | 0.8% | 11.8% | 0 |
| Open Platform | `seL4_LowLevelEthernetDriver_LowLevelEthernetDriver` | component | 18 | 0 | 283 | 4 | 5 | 1.3% | 0.0% | 0 |
| Open Platform | `seL4_MavlinkFirewall_MavlinkFirewall` | component | 26 | 0 | 691 | 122 | 5 | 1.3% | 0.4% | 0 |
| Open Platform | `mavlink_parser_vest` | library | 216 | 0 | 2532 | 1635 | 5 | 0.6% | 0.8% | 0 |
| Open Platform | `vest_lib` | library | 3177 | 0 | 20757 | 39198 | 5 | 0.7% | 0.5% | 0 |
| Open Platform | `seL4_RxFirewall_RxFirewall` | component | 40 | 0 | 4433 | 4036 | 5 | 0.2% | 0.2% | 0 |
| Open Platform | `data` | library | 8 | 0 | 220 | 0 | 5 | 1.2% | 0.0% | 0 |
| Open Platform | `GumboLib` | library | 0 | 0 | 231 | 0 | 5 | 0.4% | 0.0% | 0 |
| Open Platform | `firewall-core` | library | 39 | 0 | 578 | 291 | 5 | 0.4% | 0.4% | 0 |
| Open Platform | `seL4_TxFirewall_TxFirewall` | component | 20 | 0 | 971 | 650 | 5 | 0.7% | 0.9% | 0 |
| Isolette | `operator_interface_oip_oit` | component | 22 | 0 | 265 | 12 | 5 | 0.6% | 5.9% | 0 |
| Isolette | `data` | library | 20 | 0 | 219 | 0 | 5 | 1.9% | 0.0% | 0 |
| Isolette | `GUMBO_Library` | library | 0 | 0 | 182 | 0 | 5 | 2.2% | 0.0% | 0 |
| Isolette | `thermostat_mt_dmf_dmf` | component | 7 | 0 | 202 | 0 | 5 | 1.3% | 0.0% | 0 |
| Isolette | `thermostat_mt_ma_ma` | component | 15 | 0 | 258 | 6 | 5 | 0.3% | 7.2% | 0 |
| Isolette | `thermostat_mt_mmi_mmi` | component | 18 | 0 | 285 | 17 | 5 | 0.7% | 3.1% | 0 |
| Isolette | `thermostat_mt_mmm_mmm` | component | 14 | 0 | 252 | 5 | 5 | 0.7% | 11.9% | 0 |
| Isolette | `thermostat_rt_drf_drf` | component | 7 | 0 | 199 | 0 | 5 | 0.7% | 0.0% | 0 |
| Isolette | `thermostat_rt_mhs_mhs` | component | 15 | 0 | 250 | 4 | 5 | 0.2% | 10.6% | 0 |
| Isolette | `thermostat_rt_mri_mri` | component | 19 | 0 | 297 | 23 | 5 | 0.7% | 3.8% | 0 |
| Isolette | `thermostat_rt_mrm_mrm` | component | 14 | 0 | 245 | 4 | 5 | 0.8% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic` | component | 15 | 0 | 233 | 2 | 5 | 0.5% | 20.3% | 0 |
| RTS | `data` | library | 0 | 0 | 158 | 0 | 5 | 1.5% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic` | component | 15 | 0 | 233 | 2 | 5 | 1.2% | 20.3% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic` | component | 11 | 0 | 216 | 1 | 5 | 0.4% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic` | component | 15 | 0 | 234 | 2 | 5 | 0.5% | 20.3% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic` | component | 15 | 0 | 233 | 2 | 5 | 0.3% | 20.3% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic` | component | 15 | 0 | 231 | 2 | 5 | 1.2% | 20.3% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic` | component | 11 | 0 | 215 | 1 | 5 | 0.3% | 0.0% | 0 |
| RTS | `actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic` | component | 15 | 0 | 232 | 2 | 5 | 0.4% | 0.0% | 0 |
| RTS | `actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic` | component | 11 | 0 | 215 | 1 | 5 | 1.6% | 0.0% | 0 |
| RTS | `actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator` | component | 11 | 0 | 215 | 1 | 5 | 0.4% | 0.0% | 0 |
| RTS | `actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic` | component | 11 | 0 | 215 | 1 | 5 | 0.5% | 0.0% | 0 |
| RTS | `actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator` | component | 11 | 0 | 216 | 1 | 5 | 1.5% | 0.0% | 0 |
| RTS | `actuatorsMock_actuatorsMockThread` | component | 10 | 0 | 206 | 0 | 5 | 0.6% | 0.0% | 0 |
| RTS | `eventControlMock_eventControlMockThread` | component | 10 | 0 | 218 | 2 | 5 | 0.3% | 0.0% | 0 |
| RTS | `instrumentationMock_instrumentationMockThread` | component | 33 | 0 | 544 | 71 | 5 | 0.5% | 1.6% | 0 |

<details>
<summary>Key</summary>

Columns, left to right:

- **Case study**: the system.
- **Crate**: the Cargo package name.
- **Role**: *component* = a crate verified through its own `make verus` target (the thread crates, and Isolette's test controller and system-proof crate); *library* = a library crate (`data`, the GUMBO library crate, `firewall-core`, `mavlink_parser_vest`, and the third-party `vest_lib`), measured while verifying one crate that depends on it.
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
No crate with a median of at least 100 ms has a coefficient of variation above 5% (largest: `FirewallRx_FirewallRx` 2.5%, `GUMBO_Library` 2.2%, `data` 1.9%). **Recommendation:** 5 runs are sufficient; more runs would not change the medians materially.

<details>
<summary>Key</summary>

- **Median total (ms)**: median Verus total time of the crate.
- **CV total**: coefficient of variation of its Verus total time.
- **Runs for +-5% (95% CI)**: runs needed for the 95% confidence interval of the mean Verus total time to be within +-5% of the mean, assuming normally distributed times: ceil((1.96 * CV / 0.05)^2).

</details>

