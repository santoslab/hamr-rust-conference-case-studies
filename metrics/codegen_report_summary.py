#!/usr/bin/env python3
"""Summarize HAMR codegen reports (metrics/codegen-reports/<case>.json) for the paper.

The reports come from a domain-scheduler, Verus-macro-syntax codegen run of each case
study's unmodified model (see metrics/README.md): HAMR does not yet write the report for
user-land (MCS) builds or for --verus-attribute-syntax. Architecture and GUMBO content
come from the model and so are the same as for the case studies' own builds.

Reported per case study:
  * threads (instances and distinct thread types), ports by kind/direction
  * GUMBO logical units by kind, per thread type and in total
  * generated Verus contract lines: the source span of each GUMBO clause's Verus
    translation in the generated code of that report's build

Output: metrics/codegen_report_summary.md (and .csv). Usage: python3 metrics/codegen_report_summary.py
"""
import csv, json, os
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
CASES = OrderedDict([("BASS", "bass"), ("Open Platform", "open-platform"),
                     ("Isolette", "isolette"), ("RTS", "rts")])
# GUMBO kinds in report order: (column title, path into GumboReport)
KINDS = [
    ("state vars", ("stateReport",)),
    ("functions", ("methodsReport",)),
    ("invariants", ("invariantsReport",)),
    ("integ. assume", ("integrationReport", "assumesReport")),
    ("integ. guarantee", ("integrationReport", "guaranteesReport")),
    ("init guarantee", ("initializeReport",)),
    ("compute assume", ("computeReport", "assumesReport")),
    ("compute guarantee", ("computeReport", "guaranteesReport")),
    ("compute case", ("computeReport", "casesReport")),
    ("handler", ("computeReport", "handlers")),
]
# kinds that are contract clauses (state vars and GUMBO functions are declarations)
CLAUSE_KINDS = [k for k, _ in KINDS if k not in ("state vars", "functions")]


def opt(x):
    """unwrap a serialized Option (None -> None)"""
    if isinstance(x, dict) and x.get("type") == "None":
        return None
    if isinstance(x, dict) and x.get("type") == "Some":
        return x["value"]
    return x


def entries(gumbo, path):
    x = gumbo
    for p in path:
        x = opt(x.get(p)) if isinstance(x, dict) else None
        if x is None:
            return []
    return x.get("entries", [])


def span(pos):
    return pos["endLine"] - pos["beginLine"] + 1


def summarize(report_file):
    r = json.load(open(report_file))
    mk = [v for k, v in r["reports"]["entries"] if isinstance(v, dict) and "componentReport" in v][0]
    threads = []
    for _, c in mk["componentReport"]["entries"]:
        if c["kind"]["value"] != "Thread":
            continue
        g = opt(c.get("gumboReport"))
        counts = Counter()
        lines = Counter()
        if g:
            for kind, path in KINDS:
                es = entries(g, path)
                counts[kind] += len(es)
                if kind in CLAUSE_KINDS:
                    lines[kind] += sum(span(p) for _, p in es)
        ports = Counter((p["kind"]["value"], p["direction"]["value"]) for _, p in c["ports"]["entries"])
        threads.append({"instance": ".".join(c["path"][1:]), "type": c["modelImplementation"]["id"],
                        "ports": ports, "gumbo": counts, "verus_lines": lines})
    return threads

# the GUMBO columns, in table order (name, definition)
KIND_COLS = [
    ("state vars", "GUMBO `state` variable declarations."),
    ("functions", "GUMBO functions (`def` / `@spec def`) declared in the thread's own GUMBO block (functions of "
     "GUMBO library packages are not included; see `sysml_loc.md`)."),
    ("invariants", "GUMBO `invariants` clauses."),
    ("integ. assume", "`integration` `assume` clauses (constraints on values arriving on input ports)."),
    ("integ. guarantee", "`integration` `guarantee` clauses (constraints on values sent on output ports)."),
    ("init guarantee", "`initialize` `guarantee` clauses."),
    ("compute assume", "`compute` `assume` clauses (general preconditions of the compute entry point)."),
    ("compute guarantee", "`compute` `guarantee` clauses (general postconditions)."),
    ("compute case", "`compute` `case` clauses (each an assume / guarantee pair)."),
    ("handler", "event-port `handle` clauses (sporadic threads)."),
    ("Clauses", "sum of invariants, integ. assume, integ. guarantee, init guarantee, compute assume, compute "
     "guarantee, compute case and handler (state vars and functions are declarations, not clauses)."),
    ("Verus lines", "number of source lines of the Verus code HAMR generated for those clauses (each clause's "
     "position in the generated Rust as recorded in the report, end line - begin line + 1; measured in the "
     "macro-syntax build the report came from, see `README.md`)."),
]


def key(columns, notes=()):
    """a collapsible key: the table's columns in order, then notes (GitHub renders <details>)"""
    out = ["", "<details>", "<summary>Key</summary>", "", "Columns, left to right:", ""]
    out += [f"- **{n}**: {t}" for n, t in columns]
    for x in notes:
        out += ["", x]
    return out + ["", "</details>", ""]


def main():
    md, rows = [], []
    md.append("# Architecture and GUMBO contract metrics (from HAMR codegen reports)\n")
    md.append("Counted from HAMR's codegen reports (see `README.md` for how they were produced). "
              "Each table is followed by a collapsible key defining its columns.\n")
    hdr = "| Case study | Threads (types) | Ports in/out | " + " | ".join(k for k, _ in KINDS) + " | Clauses | Verus lines |"
    md.append("## Per case study (all thread instances)\n")
    md.append(hdr)
    md.append("|:--|--:|--:|" + "--:|" * len(KINDS) + "--:|--:|")
    per_type_md = []
    for case, f in CASES.items():
        ts = summarize(os.path.join(ROOT, "codegen-reports", f + ".json"))
        tot = Counter(); vl = 0; pin = pout = 0
        for t in ts:
            tot.update(t["gumbo"]); vl += sum(t["verus_lines"].values())
            pin += sum(n for (k, d), n in t["ports"].items() if d == "In")
            pout += sum(n for (k, d), n in t["ports"].items() if d == "Out")
            rows.append([case, t["instance"], t["type"]] + [t["gumbo"][k] for k, _ in KINDS] +
                        [sum(t["gumbo"][k] for k in CLAUSE_KINDS), sum(t["verus_lines"].values())])
        types = OrderedDict()
        for t in ts:
            types.setdefault(t["type"], []).append(t)
        clauses = sum(tot[k] for k in CLAUSE_KINDS)
        md.append(f"| {case} | {len(ts)} ({len(types)}) | {pin}/{pout} | " +
                  " | ".join(str(tot[k]) for k, _ in KINDS) + f" | {clauses} | {vl} |")
        # per thread type (contracts are per type; instances of a type share them)
        per_type_md.append(f"\n### {case}\n")
        per_type_md.append("| Thread type | Instances | Ports in/out | " + " | ".join(k for k, _ in KINDS) + " | Clauses | Verus lines |")
        per_type_md.append("|:--|--:|--:|" + "--:|" * len(KINDS) + "--:|--:|")
        for ty, insts in types.items():
            t = insts[0]
            pi = sum(n for (k, d), n in t["ports"].items() if d == "In")
            po = sum(n for (k, d), n in t["ports"].items() if d == "Out")
            per_type_md.append(f"| `{ty}` | {len(insts)} | {pi}/{po} | " +
                               " | ".join(str(t["gumbo"][k]) for k, _ in KINDS) +
                               f" | {sum(t['gumbo'][k] for k in CLAUSE_KINDS)} | {sum(t['verus_lines'].values())} |")
    md += key([
        ("Case study", "the system."),
        ("Threads (types)", "number of thread instances in the system; in parentheses, the number of distinct "
         "thread definitions they instantiate."),
        ("Ports in/out", "total number of input / output ports (data, event and event-data) over all thread "
         "instances.")] + KIND_COLS,
        ["Every count is summed over all thread *instances*: the contract of a thread definition that is "
         "instantiated several times (RTS) is counted once per instance. The reports list threads only "
         "(not processes or systems)."])
    md.append("\n## Per thread type\n")
    md.extend(per_type_md)
    md += key([
        ("Thread type", "a distinct thread definition (`<package>::<part def>`)."),
        ("Instances", "how many thread instances in the system use it."),
        ("Ports in/out", "number of input / output ports of one instance.")] + KIND_COLS,
        ["One row per thread definition; all columns after Instances are for a single instance (instances of a "
         "definition share its ports and contract)."])
    open(os.path.join(ROOT, "codegen_report_summary.md"), "w").write("\n".join(md) + "\n")
    with open(os.path.join(ROOT, "codegen_report_summary.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["case_study", "thread_instance", "thread_type"] + [k for k, _ in KINDS] + ["clauses", "verus_lines"])
        w.writerows(rows)
    print("\n".join(md))


if __name__ == "__main__":
    main()
