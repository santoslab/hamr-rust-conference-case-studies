# HAMR SysMLv2/Rust/Verus Case Studies

Case studies for the HAMR SysMLv2 → Rust/Verus → seL4 Microkit conference paper
(see [santoslab/hamr-rust-conference](https://github.com/santoslab/hamr-rust-conference)).

Each case study is a snapshot of its upstream source, copied at the commit listed
below. Only the SysMLv2 model, the HAMR Microkit output directory it targets (the MCS / user-land
scheduler variant), and (where
present) the requirements were copied; build outputs (`target/`, `.slang/`, coverage
`*.profraw`) were excluded.

| Case study | Upstream source (pinned commit) | Copied paths |
|:--|:--|:--|
| [BASS](bass/readme.md) — Basic Autonomy Security Scenario; regenerated here for the user-land scheduler | [santoslab/HAMR-agent-workflow-experiments @ `975b07c`](https://github.com/santoslab/HAMR-agent-workflow-experiments/tree/975b07c7688997290739b3707604f8574014df87/simple-open-platform-Mod-01/isolate-ethernet-simple) (2026-10-09) | `simple-open-platform-Mod-01/isolate-ethernet-simple/{sysml,hamr,requirements}` |
| [Open Platform](open-platform/readme.md) — MCS version (QEMU-simulatable) | [loonwerks/INSPECTA-Open-Platform @ `cc73dd5`](https://github.com/loonwerks/INSPECTA-Open-Platform/tree/cc73dd58840d4552c9db50ffbe3c69f86c196616/ardupilot-basic) (2026-09-25) | `ardupilot-basic/{sysml_mcs,requirements,hamr/microkit_mcs}` |
| [Isolette](isolette/readme.md) — user-land scheduler version | [loonwerks/INSPECTA-models @ `c2a471d`](https://github.com/loonwerks/INSPECTA-models/tree/c2a471dcc5675eeb8f5379bd487bc76748db1dff/isolette) (2026-10-08) | `isolette/{sysml,hamr/microkit_mcs}` |
| [RTS](rts/readme.md) — HARDENS Reactor Trip System | [santoslab/rts-showcase @ `867385f`](https://github.com/santoslab/rts-showcase/tree/867385ffa37b89d81993d1f513d9d19eb372fd50/sysmlv2/sysml) (2026-09-01) | `sysmlv2/sysml` (model only); Rust/Verus Microkit version developed here from the Slang implementation |

All four case studies use the seL4 Microkit user-land (MCS) scheduler. Where a case study
differs from its upstream source, its readme lists the changes.
