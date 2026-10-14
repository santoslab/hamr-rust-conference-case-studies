# Metrics

Scripts and data behind the paper's size and verification metrics.

| File | What it is |
|:--|:--|
| `codegen-reports/<case>.json` | HAMR codegen report for each case study (see below) |
| `codegen_report_summary.py` | Summarizes the reports: threads, ports, GUMBO logical units by kind, generated Verus contract lines |
| `codegen_report_summary.md` / `.csv` | Its output |
| `sysml_loc.py` → `sysml_loc.md` / `.csv` | SysMLv2 model and GUMBO size: code lines, GUMBO split into component contracts, data-type invariants, system-level contracts and GUMBO libraries |
| `code_loc.py` → `code_loc.md` / `.csv` / `code_loc_files.csv` | Implementation size: every Rust/C line by provenance (HAMR-generated, HAMR contract regions, HAMR template, developer, Vest-generated), Verus mode (Verus' `line_count`: spec/proof/exec/trusted) and role |
| `verus_timing.py` | Verus verification time per crate (crate only, dependencies cached; median of N runs) |

**Contents**

- [How the codegen reports were produced](#how-the-codegen-reports-were-produced)
- [Inputs for `code_loc.py`](#inputs-for-code_locpy)

## How the codegen reports were produced

HAMR writes `hamr/microkit/reporting/codegen_report_sysml.json` only for domain-scheduler
builds (it reads `microkit.system`, which user-land/MCS builds do not generate) and not for
`--verus-attribute-syntax` builds. The case studies use user-land scheduling, and Isolette
and Open Platform use attribute syntax, so each report was produced from a scratch copy of
the case study's model, unchanged except for:

- all `//@ HAMR:` configuration lines removed;
- Open Platform only: `Scheduling = MCS` removed and `Frame_Period` raised from 100 ms to
  1000 ms in `Platform.sysml` (the domain scheduler's pacer needs the longer frame).

and generated with (HAMR at Verus 0.2026.09.06)

```sh
sireum hamr sysml codegen --platform Microkit --package-name <pkg> \
  --output-dir <scratch>/hamr --sel4-output-dir <scratch>/hamr/microkit \
  --workspace-root-dir <scratch>/sysml --sourcepath <scratch>/sysml[:$SYSML_AADL_LIBRARIES] \
  --system-name <system> --no-proyek-ive <scratch>/sysml/<main>.sysml
```

| Case | `<pkg>` | `<system>` | `<main>` |
|:--|:--|:--|:--|
| bass | microkit | `SW::seL4_i` | SW |
| open-platform | firewall | `Platform::ZCU102_Impl` | Platform |
| isolette | isolette | `Isolette::Isolette_Single_Sensor` | Isolette |
| rts | RTS | `RTS::RTS_i` | RTS |

The architecture and GUMBO sections of a report come from the model and are therefore the
same as for the case study's own build. The GUMBO positions point at the Verus translation
of each clause in the scratch build's generated Rust (macro syntax): exact for BASS and RTS,
which also use macro syntax, and within a few lines for Isolette and Open Platform, whose
attribute-syntax translations are formatted slightly differently.

The reports cover threads only (no processes, systems or connections), and GUMBO functions
declared in library packages (`GumboLib.sysml`, `GUMBO_Library.sysml`) are not included in
the per-thread `functions` counts.

## Inputs for `code_loc.py`

- Verus' `line_count`: the `line_count` binary from the Verus release zip
  (`verus-0.2026.09.06.8dea4a2-<platform>.zip`; provers-env prunes it from `~/provers/verus`).
- A pristine generation of each case study, used to tell HAMR's template lines from the
  developer's in generate-once files: the case study's model regenerated with the same
  command line as the case study (see each case study's readme) into an empty directory.

```sh
python3 metrics/code_loc.py --line-count <line_count> \
  --pristine bass=<dir>/hamr/microkit_mcs --pristine open-platform=<dir>/hamr/microkit_mcs \
  --pristine isolette=<dir>/hamr/microkit_mcs --pristine rts=<dir>/hamr/microkit_mcs
```
