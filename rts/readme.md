# RTS — Reactor Trip System (HARDENS Actuation Subsystem), Rust/Verus version

HAMR-compatible SysMLv2 version of the Galois HARDENS Actuation Subsystem, with GUMBO
contracts on the CoincidenceLogic, OrLogic, and Actuator threads.

**Source:** [santoslab/rts-showcase @ `867385ffa37b89d81993d1f513d9d19eb372fd50`](https://github.com/santoslab/rts-showcase/tree/867385ffa37b89d81993d1f513d9d19eb372fd50/sysmlv2/sysml)
(path `sysmlv2/sysml`; model only).

- Model: [sysml/RTS.sysml](sysml/RTS.sysml), [sysml/Actuation.sysml](sysml/Actuation.sysml) — regenerate with
  `sysml/bin/run-hamr.cmd` (needs `SYSML_AADL_LIBRARIES` pointing at the SysML AADL libraries)
- Microkit/Rust: [hamr/microkit_mcs](hamr/microkit_mcs) — user-land (MCS) scheduler

## Changes from upstream

The upstream model targets Slang (JVM / Linux / seL4-CAmkES). This version targets Rust
on seL4 Microkit:

- `RTS.sysml`: the `//@ HAMR:` lines now select Microkit with the user-land scheduler;
  `Periodic_Thread` sets `Implementation_Language = Rust`; the three mock processes are
  assigned scheduling domains 2–4.
- `Actuation.sysml`: Microkit requires a unique scheduling domain per process. The AADL
  model expresses this with `CASE_Scheduling::Domain_Mapping` on instance paths, which has
  no SysML counterpart, and HAMR's SysML front end does not pick up `Domain` set through a
  nested redefinition on a part usage. The per-instance domains (5–16, matching the AADL
  model) are therefore attached via specialized part definitions
  (`ActuationLogicUnit1_i :> ActuationLogicUnit_i`, etc.). GUMBO contracts are unchanged.
- The component behavior in `hamr/microkit_mcs/crates/*/src/component/*_app.rs` is a
  port of the upstream Slang implementations
  (`sysmlv2/hamr/slang/src/main/component/RTS/**`): 2-of-4 coincidence voting, 2-input OR,
  and actuator logic, plus the instrumentation / event-control / actuators mocks with the
  same test vectors. The Slang code uses the non-short-circuit `&`/`|`; Verus does not
  support those on `bool`, so the Rust uses `&&`/`||` (equivalent for these
  side-effect-free operands).

## Verifying the instrumentation mock

All RTS crates verify with plain `make verus` except
`hamr/microkit_mcs/crates/instrumentationMock_instrumentationMockThread`, which is verified
with:

```sh
CARGO_VERUS_OPTS="--fwd-verus-args-to roots" \
SMT_OPTS="--rlimit 100 --smt-option smt.random_seed=7 --smt-option smt.relevancy=0" \
make verus
```

The mock has 24 `bool` output ports. For each port HAMR generates a `put_*` bridge method
whose contract states that the other ports are unchanged. With Verus 0.2026.09.x's
encoding of the `&mut self` update, Z3's default search case-splits on the struct's `bool`
fields, so the cost of each `put_*` roughly doubles with every additional port: trivial at
the 2--5 ports of the other RTS components, but not finishing at 24 ports.
`smt.relevancy=0` makes Z3 skip that splitting, and the crate verifies in well under a
second. It changes how Z3 searches, not what is proved.

The option cannot simply be added to `SMT_OPTS`, because cargo-verus passes `SMT_OPTS` to
every crate it verifies, including `vstd`, whose proofs fail with `smt.relevancy=0`.
`CARGO_VERUS_OPTS="--fwd-verus-args-to roots"` restricts the forwarded options to this
crate, so `vstd` is still verified, with Verus' default settings.
