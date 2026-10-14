# BASS — Basic Autonomy Security Scenario (user-land scheduler version)

The paper's running example: a simplified Open Platform with Rx/Tx firewalls guarding
ArduPilot, plus a ModeManager thread.

**Source:** [santoslab/HAMR-agent-workflow-experiments @ `975b07c7688997290739b3707604f8574014df87`](https://github.com/santoslab/HAMR-agent-workflow-experiments/tree/975b07c7688997290739b3707604f8574014df87/simple-open-platform-Mod-01/isolate-ethernet-simple)
(path `simple-open-platform-Mod-01/isolate-ethernet-simple`; copied `sysml/`, `hamr/`, `requirements/`).

- Model: [sysml/SW.sysml](sysml/SW.sysml) — regenerate with `sysml/bin/run-hamr.cmd`
- Microkit/Rust: [hamr/microkit_mcs](hamr/microkit_mcs)

## Changes from upstream

Upstream only provides a domain-scheduler build (`hamr/microkit`). Here BASS was
regenerated with the user-land (MCS) scheduler to match the other case studies:

- `sysml/SW.sysml` `//@ HAMR:` line: added `--scheduling UserLand`, output to
  `hamr/microkit_mcs`. The model itself (including all GUMBO contracts) is unchanged.
- `sysml/bin/run-hamr.cmd` rewritten to generate only the paper's target (Rust on seL4
  Microkit with the user-land scheduler) by default, in the style of INSPECTA-models'
  scripts; upstream's version also drove the JVM/Slang and C targets.
- `sysml/bin/clean.cmd` added (INSPECTA-models' Isolette clean script, plus the proptest
  regression seeds in its keep-list).
- `hamr/microkit_mcs` was generated fresh with current HAMR; the developer-written files
  were carried over unchanged from upstream `hamr/microkit`: the FirewallRx, FirewallTx and
  ModeManager `*_app.rs` and `test/tests.rs`, and FirewallRx's `proptest-regressions`.
  All other generate-once files (Cargo.toml, rust-toolchain.toml, GumboLib, the other app
  stubs) were identical to the HAMR templates upstream and so were taken from the new
  generation, which moves the crates to Verus 0.2026.09.06 / Rust 1.98.0.
- `hamr/slang` removed: stale Slang output from an earlier single-firewall version of BASS that upstream
  still carried; it is not part of the Microkit build.
- Codegen re-wove the generated contract regions of the app files; the only change there
  is that newer HAMR writes `final(api)` / `final(self)` in `ensures` clauses.
- FirewallTx's `test/tests.rs`: the specification-audit tests `audit_F1a` and `audit_F1b`
  were written to *pass* while HAMR's executable test oracle (GUMBOX) for
  RC_INSPECTA_00_HLR_14 accepted forwarding a malformed IPv4 frame, an operator-precedence
  error in the generated Rust. Current HAMR generates that oracle correctly, so the two tests
  now check that the oracle *rejects* the forward (renamed
  `audit_F1a_malformed_ipv4_forward_rejected_clause_level` and
  `audit_F1b_malformed_ipv4_forward_rejected_full_post`), and the audit comment records the
  fix.

Status: `make verus` (all 5 crates verify), `make test` (118 tests pass), and `make`
(image builds) succeed.
