# SysMLv2 model and GUMBO contract size

Size of each case study's own `.sysml` files; the table is followed by a key defining its columns.

| Case study | Files | Total lines | Model code (excl. GUMBO) | GUMBO component code (descr.) | GUMBO component blocks | GUMBO component defs | GUMBO datatype code (blocks) | GUMBO system code (descr.) | GUMBO system defs | GUMBO library code (descr.) | GUMBO library defs |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| BASS | 2 | 465 | 155 | 137 (0) | 3 | 0 | 7 (1) | 0 (0) | 0 | 17 (0) | 13 |
| Open Platform | 3 | 830 | 382 | 171 (0) | 3 | 3 | 0 (0) | 0 (0) | 0 | 135 (0) | 49 |
| Isolette | 11 | 2366 | 582 | 415 (91) | 7 | 8 | 18 (3) | 415 (4) | 9 | 28 (0) | 11 |
| RTS | 5 | 527 | 372 | 30 (4) | 3 | 0 | 0 (0) | 0 (0) | 0 | 0 (0) | 0 |
| ICS | 5 | 993 | 549 | 202 (0) | 9 | 5 | 0 (0) | 0 (0) | 0 | 58 (0) | 8 |

<details>
<summary>Key</summary>

Columns, left to right:

- **Case study**: the system.
- **Files**: number of the case study's own `*.sysml` model files (the AADL / HAMR SysML library packages are not counted).
- **Total lines**: all lines of those files, including comments and blank lines.
- **Model code (excl. GUMBO)**: code lines outside GUMBO blocks: packages, part / port / attribute definitions, connections, allocations and properties.
- **GUMBO component code (descr.)**: code lines of the GUMBO blocks attached to thread definitions, i.e. the component contracts. In parentheses: how many of those lines are only requirement description text (continuation lines of a multi-line description string), i.e. documentation rather than formal contract text.
- **GUMBO component blocks**: number of those component GUMBO blocks, i.e. contracted thread definitions (a thread definition instantiated several times counts once).
- **GUMBO component defs**: GUMBO function declarations (`def` or `@spec def`) inside the component blocks.
- **GUMBO datatype code (blocks)**: code lines of GUMBO blocks attached to data-type definitions (`part def ... :> Data`), i.e. data-type invariants; in parentheses the number of such blocks.
- **GUMBO system code (descr.)**: code lines of GUMBO blocks attached to system definitions (`part def ... :> System`), i.e. system-level contracts and properties; in parentheses the lines that are only description text.
- **GUMBO system defs**: GUMBO function declarations inside the system-level blocks.
- **GUMBO library code (descr.)**: code lines of GUMBO blocks attached to a `package`, i.e. GUMBO library packages (`GumboLib`, `GUMBO_Library`); in parentheses the lines that are only description text.
- **GUMBO library defs**: GUMBO function declarations inside the library blocks.

**Counting.** A *code line* has at least one character that is neither whitespace nor part of a comment (`//` to end of line, or `/* ... */`); string literals count as code. (Same rule as the PROVERS effort measurer, spec M-7.)

**GUMBO blocks.** A GUMBO block runs from a `language "GUMBO" /*{` line to the matching `}*/` line; both of those lines are counted as code. A block belongs to the nearest preceding `part def` or `package`, which decides whether it is counted as component, datatype, system or library GUMBO.

</details>

