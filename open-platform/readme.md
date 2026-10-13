# Open Platform (MCS version)

Collins INSPECTA Open Platform cyber-retrofit: ArduPilot in a VM, guarded by Rx/Tx and
MAVLink firewalls written in Rust and verified with Verus. This is the MCS-scheduled
variant, which can be simulated under QEMU (`qemu-virtio` driver feature) as well as
built for the ZCU102.

**Source:** [loonwerks/INSPECTA-Open-Platform @ `cc73dd58840d4552c9db50ffbe3c69f86c196616`](https://github.com/loonwerks/INSPECTA-Open-Platform/tree/cc73dd58840d4552c9db50ffbe3c69f86c196616/ardupilot-basic)
(path `ardupilot-basic`; copied `sysml_mcs/`, `requirements/`, `hamr/microkit_mcs/`).

- Model: [sysml_mcs/Platform.sysml](sysml_mcs/Platform.sysml), [sysml_mcs/SW.sysml](sysml_mcs/SW.sysml) — regenerate with `sysml_mcs/bin/clean.cmd` followed by
  `sysml_mcs/bin/run-hamr.cmd --platform Microkit --scheduling UserLand --verus-attribute-syntax --sel4-output-dir <abs path>/hamr/microkit_mcs`
- Microkit/Rust: [hamr/microkit_mcs](hamr/microkit_mcs)

Relation to the upstream domain-scheduler variant (`sysml/` + `hamr/microkit/`): the
GUMBO contracts are identical (models differ only in timing, `Scheduling = MCS`, and
processor bindings), and the component behavior code and Verus `timeTriggered`
contracts are semantically equivalent. The domain-scheduler `hamr/microkit` was last
regenerated from an earlier model that still carried two integration assumptions since
removed from both models; the MCS output matches the current model.

## Changes from upstream

- `sysml_mcs/bin/run-hamr.cmd` was rewritten in the style of INSPECTA-models'
  `isolette/sysml/bin/run-hamr.cmd` (platform options are passed on the command line),
  and `sysml_mcs/bin/clean.cmd` was added. `clean.cmd` removes HAMR-generated files,
  including untouched generate-once files, so that codegen recreates them from the current
  templates; its keep-list preserves all developer code and developer-modified files
  (`firewall_core`, `mavlink_parser_vest`, the driver's `core` crate, the component
  manifests that add those dependencies, the ArduPilot VM board/virtio files, `meta.py`,
  the QEMU/ZCU102 makefiles).
- Regenerated with `run-hamr.cmd --platform Microkit --scheduling UserLand
  --verus-attribute-syntax --sel4-output-dir hamr/microkit_mcs` against Verus
  0.2026.09.06 (the Verus release Vest targets). The developer-maintained manifests were
  moved to the same Verus crates, and `vest_lib` from git rev `e0671fb` to the crates.io
  release `=0.2.1`; `firewall_core`'s toolchain moved from Rust 1.97.1 to 1.98.0. No code
  changes were needed for the Vest move.
- `crates/seL4_LowLevelEthernetDriver_LowLevelEthernetDriver/src/component/..._app.rs`:
  added a `#[verifier::external_type_specification]` for `QemuVirtioDriver`, mirroring
  the existing one for the ZCU102 `Driver`. Without it `make verus` fails for the QEMU
  configuration (`MICROKIT_BOARD=qemu_virt_aarch64`), because the type is declared outside
  `verus!`.
