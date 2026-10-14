# ICS Status - Intrinsic Cognitive Security Status

Collins hardened MATRICS Status model (under DARPA's ICS program). The
ground station communicates with a head-mounted display and includes Wi-Fi,
Bluetooth, and USB interfaces; encrypted log storage and analysis; and GUMBO
contracts for its monitoring, reporting, firewall, and zeroization behavior.

**Source:** [loonwerks/MATRICS @ `fd543d1`](https://github.com/loonwerks/MATRICS/commit/fd543d127724b21d7ac0b33df670097236c4197c)
(path `Models/Status/Status_v2/Hardened/withAGREEAndGumbo`; copied `sysml/`,
`hamr/microkit_mcs_sysml/`).

- **Model:** [`sysml/`](sysml/) contains the Status scenario and the
  `GroundStation::GroundStation_Impl` system targeted by HAMR. Run
  [`sysml/bin/run-hamr.cmd`](sysml/bin/run-hamr.cmd) to regenerate the code.
- **Microkit/Rust:** [`hamr/microkit_mcs/`](hamr/microkit_mcs/) contains the
  generated Rust/Verus implementation for the seL4 Microkit user-land (MCS)
  scheduler.

The model and implementation are an unchanged snapshot of the pinned upstream
commit. The upstream generated directory, `microkit_mcs_sysml`, is named
`microkit_mcs` here to match the layout used by the other case studies.
