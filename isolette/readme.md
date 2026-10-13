# Isolette (user-land scheduler version)

Infant incubator temperature controller (FAA Requirements Engineering Management Handbook).

**Source:** [loonwerks/INSPECTA-models @ `c2a471dcc5675eeb8f5379bd487bc76748db1dff`](https://github.com/loonwerks/INSPECTA-models/tree/c2a471dcc5675eeb8f5379bd487bc76748db1dff/isolette)
(path `isolette`; copied `sysml/`, `hamr/microkit_mcs/`).

- Model: [sysml/Isolette.sysml](sysml/Isolette.sysml)
- Microkit/Rust: [hamr/microkit_mcs](hamr/microkit_mcs) — regenerate with `sysml/bin/clean.cmd` followed by

  ```
  sireum slang run sysml/bin/run-hamr.cmd --platform Microkit --scheduling UserLand \
    --verus-attribute-syntax --experimental-options DISABLE_SYSTEM_VERIFICATION --sel4-output-dir <abs path>/hamr/microkit_mcs
  ```

Relation to the upstream domain-scheduler variant (`hamr/microkit/`): both are generated
from the same model; component behavior code, Verus contracts, and GUMBOX contracts are
semantically equivalent (differences are Verus attribute-vs-macro syntax and logging).

## Changes from upstream

- Runtime monitoring is disabled for the paper's version: upstream generates
  `hamr/microkit_mcs` with `--runtime-monitoring` (see `isolette/.ci/ci.cmd` upstream);
  here it is generated without it. The GUMBO, system-property and user-land monitors
  (`crates/{gumbo_monitor,sys_nominal_monitor,userland_monitor}`, their `components/`
  and `scheduler/` variants and `*.mk` / `*.meta.py` build configurations) are therefore
  absent, including upstream's developer-written user-land monitor
  (`userland_monitor_process_userland_monitor_thread_app.rs`).
- The test scheduler is disabled: upstream generates with `ENABLE_TEST_SCHEDULER`; here it
  is omitted, so the test controller (`crates/test_controller`, its system tests, `bin/`
  and the `test_scheduler.*` build configurations) and the shared `crates/observers` are
  absent.
- The system-level verification crate (`crates/sys_nominal_proof`, generated from the
  model's GUMBO system compositions) is not generated (`--experimental-options
  DISABLE_SYSTEM_VERIFICATION`, which needs a HAMR build that has this option). The
  system-level GUMBO remains in the model.
- `sysml/Isolette.sysml`: the upstream `//@ HAMR:` lines (JVM/Slang outputs and Microkit
  with `--runtime-monitoring`) are replaced by one line matching the build above.
- `sysml/bin/clean.cmd` added (upstream's `isolette/aadl/bin/clean.cmd`).
- Regenerated against Verus 0.2026.09.06; all crates verify.
