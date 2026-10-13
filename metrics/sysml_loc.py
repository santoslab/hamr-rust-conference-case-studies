#!/usr/bin/env python3
"""Size of each case study's SysMLv2 model and its GUMBO contracts.

Counts the case study's own top-level *.sysml files (not copies of the AADL/HAMR SysML
libraries). Lines are classified code/comment/blank with the c-style rules of the
PROVERS effort framework's measurer (HAMR-agent-workflow-experiments,
docs/effort-measurement-spec.md M-7: a line with any code counts as code, `//` and
`/* */` are comments, string literals are code). GUMBO blocks (`language "GUMBO" /*{`
... `}*/`) are split out (M-11; the two wrapper lines count as code) and attributed to
their owner (M-12): the nearest preceding `part def` (a component contract) or `package`
(a GUMBO library). Within GUMBO, lines that are only part of a requirement description
string are reported separately, as are `def` lines (GUMBO function declarations).

Output: metrics/sysml_loc.md (and .csv). Usage: python3 metrics/sysml_loc.py
"""
import csv, glob, os, re
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = OrderedDict([("BASS", "bass/sysml"), ("Open Platform", "open-platform/sysml_mcs"),
                     ("Isolette", "isolette/sysml"), ("RTS", "rts/sysml")])
GUMBO_OPEN = re.compile(r'language\s+"GUMBO"\s*/\*\{')
GUMBO_CLOSE = "}*/"
PART_DEF = re.compile(r"\bpart\s+def\s+(\w+)")
PACKAGE = re.compile(r"\bpackage\s+(\w+)")
GUMBO_DEF = re.compile(r"^\s*(@\w+\s+)*def\s+\w+")   # incl. @spec def


def classify_c(lines):
    """c-style classification -> list of 'code'/'comment'/'blank' plus, per line, whether
    the line is entirely inside a string literal that began on an earlier line"""
    out, in_string_only = [], []
    in_block = in_str = False
    for line in lines:
        started_in_str = in_str
        if not line.strip():
            out.append("blank"); in_string_only.append(False); continue
        code = comment = False
        only_str = in_str
        i = 0
        while i < len(line):
            ch = line[i]
            if in_block:
                if line.startswith("*/", i):
                    in_block = False; i += 2; continue
                comment = True; i += 1; continue
            if in_str:
                code = True
                if ch == "\\": i += 2; continue
                if ch == '"': in_str = False; only_str = False if line[i + 1:].strip() else only_str
                i += 1; continue
            if ch.isspace(): i += 1; continue
            if line.startswith("//", i): comment = True; break
            if line.startswith("/*", i): in_block = True; i += 2; continue
            if ch == '"': in_str = True; code = True; i += 1; continue
            code = True; only_str = False; i += 1
        out.append("code" if code else ("comment" if comment else "blank"))
        in_string_only.append(started_in_str and only_str and code)
    return out, in_string_only


def measure_file(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    # GUMBO spans
    spans, i = [], 0
    while i < len(lines):
        if GUMBO_OPEN.search(lines[i]):
            j = i
            while j < len(lines) and GUMBO_CLOSE not in lines[j]:
                j += 1
            owner = ("unknown", None)
            for k in range(i - 1, -1, -1):
                m = PART_DEF.search(lines[k])
                if m:
                    # like M-12: a part def specializing System owns a system-level contract
                    rest = lines[k][m.end():]
                    kind = ("system" if re.search(r":>\s*System\b", rest) else
                            "datatype" if re.search(r":>\s*Data\b", rest) else "component")
                    owner = (kind, m.group(1)); break
                m = PACKAGE.search(lines[k])
                if m:
                    owner = ("library", m.group(1)); break
            spans.append((i, j, owner)); i = j + 1
        else:
            i += 1
    in_span = [None] * len(lines)
    for s, e, owner in spans:
        for k in range(s, e + 1):
            in_span[k] = owner[0]
    model_cls, _ = classify_c([l if in_span[n] is None else "" for n, l in enumerate(lines)])
    res = Counter()
    for n, c in enumerate(model_cls):
        if in_span[n] is None:
            res[f"model_{c}"] += 1
    for s, e, owner in spans:
        kind = owner[0]
        interior = lines[s + 1:e]
        cls, str_only = classify_c(interior)
        res[f"gumbo_{kind}_code"] += 2 + sum(1 for c in cls if c == "code")   # wrappers count as code
        res[f"gumbo_{kind}_comment"] += sum(1 for c in cls if c == "comment")
        res[f"gumbo_{kind}_blank"] += sum(1 for c in cls if c == "blank")
        res[f"gumbo_{kind}_description"] += sum(1 for c, so in zip(cls, str_only) if c == "code" and so)
        res[f"gumbo_{kind}_defs"] += sum(1 for l in interior if GUMBO_DEF.match(l))
        res[f"gumbo_{kind}_blocks"] += 1
    res["lines"] = len(lines)
    return res


def main():
    md = ["# SysMLv2 model and GUMBO contract size\n",
          "Size of each case study's own `.sysml` files; the table is followed by a key defining its columns.\n",
          "| Case study | Files | Total lines | Model code (excl. GUMBO) | GUMBO component code (descr.) | "
          "GUMBO component blocks | GUMBO component defs | GUMBO datatype code (blocks) | "
          "GUMBO system code (descr.) | GUMBO system defs | GUMBO library code (descr.) | GUMBO library defs |",
          "|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    rows = []
    for case, rel in CASES.items():
        files = sorted(glob.glob(os.path.join(ROOT, rel, "*.sysml")))
        tot = Counter()
        for f in files:
            r = measure_file(f)
            tot.update(r)
            rows.append([case, os.path.relpath(f, ROOT)] + [r[k] for k in COLS])
        md.append(f"| {case} | {len(files)} | {tot['lines']} | {tot['model_code']} | "
                  f"{tot['gumbo_component_code']} ({tot['gumbo_component_description']}) | {tot['gumbo_component_blocks']} | "
                  f"{tot['gumbo_component_defs']} | "
                  f"{tot['gumbo_datatype_code']} ({tot['gumbo_datatype_blocks']}) | "
                  f"{tot['gumbo_system_code']} ({tot['gumbo_system_description']}) | {tot['gumbo_system_defs']} | "
                  f"{tot['gumbo_library_code']} ({tot['gumbo_library_description']}) | {tot['gumbo_library_defs']} |")
        if tot["gumbo_unknown_code"]:
            md.append(f"\nWARNING: {case} has {tot['gumbo_unknown_code']} GUMBO lines with no owner\n")
    cols = [
        ("Case study", "the system."),
        ("Files", "number of the case study's own `*.sysml` model files (the AADL / HAMR SysML library packages "
         "are not counted)."),
        ("Total lines", "all lines of those files, including comments and blank lines."),
        ("Model code (excl. GUMBO)", "code lines outside GUMBO blocks: packages, part / port / attribute "
         "definitions, connections, allocations and properties."),
        ("GUMBO component code (descr.)", "code lines of the GUMBO blocks attached to thread definitions, i.e. "
         "the component contracts. In parentheses: how many of those lines are only requirement description "
         "text (continuation lines of a multi-line description string), i.e. documentation rather than formal "
         "contract text."),
        ("GUMBO component blocks", "number of those component GUMBO blocks, i.e. contracted thread definitions "
         "(a thread definition instantiated several times counts once)."),
        ("GUMBO component defs", "GUMBO function declarations (`def` or `@spec def`) inside the component blocks."),
        ("GUMBO datatype code (blocks)", "code lines of GUMBO blocks attached to data-type definitions "
         "(`part def ... :> Data`), i.e. data-type invariants; in parentheses the number of such blocks."),
        ("GUMBO system code (descr.)", "code lines of GUMBO blocks attached to system definitions "
         "(`part def ... :> System`), i.e. system-level contracts and properties; in parentheses the lines that are "
         "only description text."),
        ("GUMBO system defs", "GUMBO function declarations inside the system-level blocks."),
        ("GUMBO library code (descr.)", "code lines of GUMBO blocks attached to a `package`, i.e. GUMBO library "
         "packages (`GumboLib`, `GUMBO_Library`); in parentheses the lines that are only description text."),
        ("GUMBO library defs", "GUMBO function declarations inside the library blocks."),
    ]
    md += ["", "<details>", "<summary>Key</summary>", "", "Columns, left to right:", ""]
    md += [f"- **{n}**: {t}" for n, t in cols]
    md += ["",
           "**Counting.** A *code line* has at least one character that is neither whitespace nor part of a comment "
           "(`//` to end of line, or `/* ... */`); string literals count as code. (Same rule as the PROVERS effort "
           "measurer, spec M-7.)",
           "",
           "**GUMBO blocks.** A GUMBO block runs from a `language \"GUMBO\" /*{` line to the matching `}*/` line; "
           "both of those lines are counted as code. A block belongs to the nearest preceding `part def` or "
           "`package`, which decides whether it is counted as component, datatype, system or library GUMBO.",
           "", "</details>", ""]
    open(os.path.join(ROOT, "metrics", "sysml_loc.md"), "w").write("\n".join(md) + "\n")
    with open(os.path.join(ROOT, "metrics", "sysml_loc.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n"); w.writerow(["case_study", "file"] + COLS); w.writerows(rows)
    print("\n".join(md))


COLS = ["lines", "model_code", "model_comment", "model_blank",
        "gumbo_component_code", "gumbo_component_comment", "gumbo_component_blank",
        "gumbo_component_description", "gumbo_component_defs", "gumbo_component_blocks",
        "gumbo_datatype_code", "gumbo_datatype_comment", "gumbo_datatype_blank",
        "gumbo_datatype_description", "gumbo_datatype_defs", "gumbo_datatype_blocks",
        "gumbo_system_code", "gumbo_system_comment", "gumbo_system_blank",
        "gumbo_system_description", "gumbo_system_defs", "gumbo_system_blocks",
        "gumbo_library_code", "gumbo_library_comment", "gumbo_library_blank",
        "gumbo_library_description", "gumbo_library_defs", "gumbo_library_blocks"]

if __name__ == "__main__":
    main()
