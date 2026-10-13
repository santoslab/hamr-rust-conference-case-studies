#!/usr/bin/env python3
"""Measure Verus verification time per crate for the HAMR SysMLv2/Rust case studies.

Method
  1. Idle baseline: CPU temperature and macOS thermal state before any work.
  2. Warm-up: every crate is verified once with its generated Makefile's settings so that
     vstd and all dependencies are verified and cached. Each case study uses one shared
     Cargo target directory (CARGO_TARGET_DIR, outside the repository), so dependencies
     are built and verified once per case study; the four case studies warm up in
     parallel. (The RTS instrumentation mock gets its own target directory: it forwards
     different Verus options to its dependencies.)
  3. Cool-down after the warm-ups, then RUNS measured rounds. A round re-verifies every
     crate once, in turn: only the crate's own Cargo fingerprint is removed (for a
     library host, also the libraries') and `make verus` (`make all` for the system-proof
     crate) is rerun with Verus' `--time`. Cargo runs one job at a time
     (CARGO_BUILD_JOBS=1) so each crate's Verus output follows its `Checking <crate>`
     line; Verus itself uses all of its threads. A cool-down precedes every measured run.
  4. Thermal record of every measured run (macmon: CPU temperature, P-cluster frequency,
     fans; ProcessInfo.thermalState) and a variability analysis that says whether more
     runs are warranted.

Cool-downs wait for the machine to return close to its idle state rather than for a
fixed time: after the warm-ups at least WARM_COOL_MIN s and until the thermal state is
nominal, the CPU is within WARM_COOL_DT degC of the idle baseline and the fans have stopped
(at most WARM_COOL_MAX s); before each measured run at least RUN_COOL_MIN s and until the
CPU is within RUN_COOL_DT degC of the baseline and the thermal state is nominal (at most
RUN_COOL_MAX s).

Requires: macmon (brew install macmon) and the thermal-state helper (compile
metrics/thermal_state.swift with `swiftc -O -o thermal_state thermal_state.swift`). Usage:
  python3 metrics/verus_timing.py --target-root <dir> --thermal-state <helper> [--runs 5]
Output: metrics/verus_timing.csv (every run, with its thermal record),
        metrics/verus_timing.md (medians, variability and recommendation).
"""
import argparse, csv, glob, json, math, os, platform, re, shutil, statistics, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_SMT = "--rlimit 100 --smt-option smt.random_seed=7"

# case study -> crates directory
CASES = {
    "BASS": "bass/hamr/microkit_mcs/crates",
    "Open Platform": "open-platform/hamr/microkit_mcs/crates",
    "Isolette": "isolette/hamr/microkit_mcs/crates",
    "RTS": "rts/hamr/microkit_mcs/crates",
}
# library crates (cargo package names) re-verified inside a host crate
# (`data` is HAMR's generated crate for the model's data types)
LIB_HOSTS = {
    ("BASS", "FirewallRx_FirewallRx"): ["data", "GumboLib"],
    ("Isolette", "operator_interface_oip_oit"): ["data", "GUMBO_Library"],
    ("Open Platform", "seL4_RxFirewall_RxFirewall"): ["data", "GumboLib", "firewall-core"],
    ("Open Platform", "seL4_MavlinkFirewall_MavlinkFirewall"): ["mavlink_parser_vest", "vest_lib"],
    ("RTS", "actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic"): ["data"],
}
# crates that are libraries rather than components, even though they have a Makefile
LIB_DIRS = {"firewall_core"}
# per-crate settings (see each case study's readme); OWN_TARGET: crates given their own target dir
EXTRA_ENV = {
    ("RTS", "instrumentationMock_instrumentationMockThread"): {
        "CARGO_VERUS_OPTS": "--fwd-verus-args-to roots",
        "SMT_EXTRA": "--smt-option smt.relevancy=0"},
    ("Open Platform", "seL4_LowLevelEthernetDriver_LowLevelEthernetDriver"): {
        "MICROKIT_BOARD": "qemu_virt_aarch64"},
}
OWN_TARGET = {("RTS", "instrumentationMock_instrumentationMockThread")}

# cool-down parameters (seconds, degC)
WARM_COOL_MIN, WARM_COOL_MAX, WARM_COOL_DT = 180, 900, 3.0
RUN_COOL_MIN, RUN_COOL_MAX, RUN_COOL_DT = 5, 120, 5.0

CHECK_RE = re.compile(r"^\s*Checking (\S+) v")
RES_RE = re.compile(r"verification results:: (\d+) verified, (\d+) errors")
TOT_RE = re.compile(r"total-time:\s+(\d+) ms")
SMT_RE = re.compile(r"total smt-run:\s+(\d+) ms")


# ---------------------------------------------------------------- thermal monitoring
class Monitor:
    """continuous macmon sampling (every 100 ms) in a background thread"""

    def __init__(self):
        self.samples = []   # (time, cpu_temp, pcpu_freq_mhz, pcpu_active_ratio, max_fan_rpm)
        self.lock = threading.Lock()
        self.proc = subprocess.Popen(["macmon", "pipe", "-i", "100"], stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, text=True)
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.proc.stdout:
            try:
                d = json.loads(line)
                s = (time.time(), d["temp"]["cpu_temp_avg"], d["pcpu_freq_mhz"], d["pcpu_active_ratio"],
                     max((f["rpm"] for f in d.get("fans", [])), default=0))
                with self.lock:
                    self.samples.append(s)
            except Exception:
                pass

    def latest(self):
        with self.lock:
            return self.samples[-1] if self.samples else None

    def window(self, t0, t1):
        with self.lock:
            return [s for s in self.samples if t0 <= s[0] <= t1]

    def stop(self):
        self.proc.terminate()


def thermal_state(helper):
    """macOS ProcessInfo.thermalState: 0 nominal, 1 fair, 2 serious, 3 critical"""
    try:
        return int(subprocess.run([helper], capture_output=True, text=True).stdout.strip())
    except Exception:
        return -1


def idle_baseline(mon, seconds=30):
    time.sleep(seconds)
    w = mon.window(time.time() - seconds, time.time())
    return statistics.median(s[1] for s in w)


def cool_down(mon, helper, baseline, dt, min_s, max_s, need_fans_off, label):
    t0 = time.time()
    time.sleep(min_s)
    while True:
        s = mon.latest()
        st = thermal_state(helper)
        ok = s is not None and s[1] <= baseline + dt and st == 0 and (not need_fans_off or s[4] == 0)
        waited = time.time() - t0
        if ok or waited >= max_s:
            if not ok:
                print(f"   {label}: cool-down capped at {waited:.0f}s (cpu {s[1]:.1f}C, state {st}, fans {s[4]})", flush=True)
            return waited, (s[1] if s else None), st
        time.sleep(2)


# ---------------------------------------------------------------- crates and runs
def package_name(crate_dir):
    for line in open(os.path.join(crate_dir, "Cargo.toml")):
        m = re.match(r'\s*name\s*=\s*"([^"]+)"', line)
        if m:
            return m.group(1)
    return os.path.basename(crate_dir)


def make_target(crate_dir):
    mk = os.path.join(crate_dir, "Makefile")
    if not os.path.isfile(mk):
        return None
    text = open(mk).read()
    if re.search(r"^verus:", text, re.M):
        return "verus"
    if re.search(r"^all:", text, re.M) and "cargo-verus verify" in text:
        return "all"
    return None


def crates(target_root):
    out = []
    for case, rel in CASES.items():
        for crate_dir in sorted(glob.glob(os.path.join(ROOT, rel, "*/"))):
            crate_dir = crate_dir.rstrip("/")
            target = make_target(crate_dir)
            if target is None or os.path.basename(crate_dir) in LIB_DIRS:
                continue
            pkg = package_name(crate_dir)
            slug = re.sub(r"\W+", "-", case.lower())
            tdir = os.path.join(target_root, slug + ("-" + pkg if (case, pkg) in OWN_TARGET else ""))
            out.append({"case": case, "dir": crate_dir, "target": target, "pkg": pkg, "target_dir": tdir,
                        "libs": LIB_HOSTS.get((case, pkg), []), "env": EXTRA_ENV.get((case, pkg), {})})
    return out


def remove_fingerprints(target_dir, packages):
    for pkg in packages:
        for name in {pkg, pkg.replace("-", "_")}:
            for fp in glob.glob(os.path.join(target_dir, "*", "debug", ".fingerprint", f"{name}-*")) + \
                      glob.glob(os.path.join(target_dir, "debug", ".fingerprint", f"{name}-*")):
                shutil.rmtree(fp, ignore_errors=True)


def run_make(c, timed):
    env = dict(os.environ)
    env["CARGO_BUILD_JOBS"] = "1"
    env["CARGO_TARGET_DIR"] = c["target_dir"]
    smt = f"{BASE_SMT} {c['env'].get('SMT_EXTRA', '')}".strip()
    env["SMT_OPTS"] = f"{smt} --time" if timed else smt
    for k, v in c["env"].items():
        if k != "SMT_EXTRA":
            env[k] = v
    t0 = time.time()
    # one pipe for both streams: Verus reports on stdout and cargo's `Checking <crate>`
    # lines go to stderr, and their interleaving is what attributes results to crates
    p = subprocess.run(["make", c["target"]], cwd=c["dir"], env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout, t0, time.time()


def parse(output):
    """crate package name -> (verified, errors, total_ms, smt_ms)"""
    out, cur = {}, None
    for line in output.splitlines():
        m = CHECK_RE.match(line)
        if m:
            cur = m.group(1)
            continue
        if cur is None:
            continue
        d = out.setdefault(cur, [None, None, None, None])
        if (m := RES_RE.search(line)):
            d[0], d[1] = int(m.group(1)), int(m.group(2))
        elif (m := TOT_RE.search(line)):
            d[2] = int(m.group(1))
        elif (m := SMT_RE.search(line)):
            d[3] = int(m.group(1))
    return {k: tuple(v) for k, v in out.items() if v[0] is not None}


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-root", required=True, help="directory for the shared Cargo target directories")
    ap.add_argument("--thermal-state", required=True, help="compiled thermal_state.swift helper")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--cases", help="comma-separated subset of case studies (default: all)")
    ap.add_argument("--warm-cool-min", type=int, default=WARM_COOL_MIN, help="minimum post-warm-up cool-down (s)")
    ap.add_argument("--report-only", metavar="LOG", help="regenerate verus_timing.md from metrics/verus_timing.csv; "
                    "LOG is the measurement's console log (for the idle baseline and warm-up failures)")
    a = ap.parse_args()
    if a.report_only:
        report_only(a.report_only)
        return
    os.makedirs(a.target_root, exist_ok=True)
    cs = crates(a.target_root)
    if a.cases:
        keep = {x.strip() for x in a.cases.split(",")}
        cs = [c for c in cs if c["case"] in keep]
    mon = Monitor()
    try:
        print(f"{len(cs)} crates; measuring idle baseline ...", flush=True)
        baseline = idle_baseline(mon)
        print(f"idle CPU temperature {baseline:.1f}C, thermal state {thermal_state(a.thermal_state)}", flush=True)

        # warm-up: case studies in parallel, crates of a case study in turn
        def warm(case):
            res = []
            for c in [c for c in cs if c["case"] == case]:
                rc, out, t0, t1 = run_make(c, timed=False)
                print(f"[warm-up] {case} {c['pkg']}: rc={rc} {t1 - t0:.0f}s", flush=True)
                res.append((c, rc, out))
            return res
        t_warm = time.time()
        cases = sorted({c["case"] for c in cs})
        with ThreadPoolExecutor(max_workers=len(cases)) as ex:
            warm_results = [r for rs in ex.map(warm, cases) for r in rs]
        failed = {(c["case"], c["pkg"]) for c, rc, _ in warm_results if rc != 0}
        for c, rc, out in warm_results:
            if rc != 0:
                print(f"WARM-UP FAILED: {c['case']} {c['pkg']}\n{out[-2000:]}", flush=True)
        print(f"warm-ups done in {time.time() - t_warm:.0f}s; cooling down ...", flush=True)
        waited, temp, st = cool_down(mon, a.thermal_state, baseline, WARM_COOL_DT, a.warm_cool_min, WARM_COOL_MAX,
                                     True, "post-warm-up")
        print(f"cooled down after {waited:.0f}s: CPU {temp:.1f}C, thermal state {st}", flush=True)

        rows = []
        measured = [c for c in cs if (c["case"], c["pkg"]) not in failed]
        for r in range(1, a.runs + 1):
            print(f"--- round {r}/{a.runs}", flush=True)
            for c in measured:
                cool_s, start_temp, st0 = cool_down(mon, a.thermal_state, baseline, RUN_COOL_DT, RUN_COOL_MIN,
                                                    RUN_COOL_MAX, False, c["pkg"])
                remove_fingerprints(c["target_dir"], [c["pkg"]] + c["libs"])
                rc, out, t0, t1 = run_make(c, timed=True)
                st1 = thermal_state(a.thermal_state)
                w = mon.window(t0, t1)
                max_temp = max((s[1] for s in w), default=None)
                peak_freq = max((s[2] for s in w), default=None)   # peak P-cluster frequency during the run
                max_fan = max((s[4] for s in w), default=None)
                res = parse(out)
                for name in [c["pkg"]] + c["libs"]:
                    v = res.get(name) or res.get(name.replace("-", "_"))
                    role = "component" if name == c["pkg"] else "library"
                    rows.append({"case_study": c["case"], "crate": name, "role": role, "round": r,
                                 "verified": v[0] if v else "", "errors": v[1] if v else "",
                                 "verus_total_ms": v[2] if v else "", "smt_ms": v[3] if v else "",
                                 "rc": rc, "cooldown_s": round(cool_s, 1), "start_temp_c": round(start_temp, 1),
                                 "max_temp_c": round(max_temp, 1) if max_temp else "",
                                 "peak_busy_pcpu_mhz": peak_freq or "", "max_fan_rpm": max_fan if max_fan is not None else "",
                                 "thermal_state_before": st0, "thermal_state_after": st1})
                print(f"   {c['case']} {c['pkg']}: rc={rc} wall {t1 - t0:.1f}s, cool {cool_s:.0f}s, "
                      f"{start_temp:.1f}->{max_temp if max_temp is None else round(max_temp, 1)}C, peak {peak_freq} MHz, state {st0}->{st1}: "
                      + ", ".join(f"{k}={res.get(k) or res.get(k.replace('-', '_'))}" for k in [c["pkg"]] + c["libs"]),
                      flush=True)
    finally:
        mon.stop()
    write_outputs(rows, a.runs, baseline, sorted(failed))


def report_only(log):
    text = open(log).read()
    baseline = float(re.search(r"idle CPU temperature ([\d.]+)C", text).group(1))
    failed = sorted(set(re.findall(r"WARM-UP FAILED: (.+?) (\S+)\n", text)))
    rows = list(csv.DictReader(open(os.path.join(ROOT, "metrics", "verus_timing.csv"))))
    for r in rows:
        for k in ("round", "verified", "errors", "verus_total_ms", "smt_ms", "peak_busy_pcpu_mhz"):
            if r[k] != "":
                r[k] = int(r[k])
    runs = max(r["round"] for r in rows)
    write_outputs(rows, runs, baseline, failed, write_csv=False)


def write_outputs(rows, runs, baseline, failed, write_csv=True):
    mdir = os.path.join(ROOT, "metrics")
    fields = ["case_study", "crate", "role", "round", "verified", "errors", "verus_total_ms", "smt_ms", "rc",
              "cooldown_s", "start_temp_c", "max_temp_c", "peak_busy_pcpu_mhz", "max_fan_rpm",
              "thermal_state_before", "thermal_state_after"]
    if write_csv:
        with open(os.path.join(mdir, "verus_timing.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)

    # throttling: macOS reported a thermal state other than nominal before or after the run. (The peak P-cluster
    # frequency is recorded in the CSV but not used: most runs last about a second, so 100 ms samples often miss
    # the burst, and in the measured data low readings were not associated with slower runs.)
    for r in rows:
        r["throttled"] = str(r["thermal_state_before"]) not in ("0", "") or str(r["thermal_state_after"]) not in ("0", "")

    agg = {}
    for r in rows:
        if r["verus_total_ms"] == "":
            continue
        a = agg.setdefault((r["case_study"], r["crate"], r["role"]),
                           {"ver": r["verified"], "err": r["errors"], "tot": [], "smt": [], "thr": 0})
        a["tot"].append(r["verus_total_ms"]); a["smt"].append(r["smt_ms"]); a["thr"] += r["throttled"]

    def cv(xs):
        m = statistics.mean(xs)
        return statistics.stdev(xs) / m if len(xs) > 1 and m > 0 else 0.0

    def runs_needed(c):   # runs for a 95% CI of the mean within +-5% (normal approximation)
        return math.ceil((1.96 * c / 0.05) ** 2)

    ver = subprocess.run([os.path.expanduser("~/provers/verus/verus"), "--version"], capture_output=True, text=True).stdout
    vline = next((l.strip() for l in ver.splitlines() if "Version" in l), "").replace("Version: ", "")
    cpu = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    model = subprocess.run(["sysctl", "-n", "hw.model"], capture_output=True, text=True).stdout.strip()
    md = ["# Verus verification time per crate", "",
          f"Verus {vline}; {cpu} ({model}), {os.cpu_count()} cores, macOS {platform.mac_ver()[0]}; idle CPU "
          f"temperature {baseline:.1f} C. Each table is followed by a collapsible key defining its columns.", "",
          "| Case study | Crate | Role | Verified | Errors | Verus total (ms) | SMT CPU time (ms) | Runs | CV total | CV SMT | Throttled runs |",
          "|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|"]
    worst = []
    for (case, name, role), a in agg.items():
        ct, cs_ = cv(a["tot"]), cv(a["smt"])
        worst.append((ct, case, name, statistics.median(a["tot"])))
        md.append(f"| {case} | `{name}` | {role} | {a['ver']} | {a['err']} | {statistics.median(a['tot']):.0f} | "
                  f"{statistics.median(a['smt']):.0f} | {len(a['tot'])} | {ct:.1%} | {cs_:.1%} | {a['thr']} |")
    md += ["", "<details>", "<summary>Key</summary>", "", "Columns, left to right:", "",
           "- **Case study**: the system.",
           "- **Crate**: the Cargo package name.",
           "- **Role**: *component* = a crate verified through its own `make verus` target (the thread crates, and "
           "Isolette's test controller and system-proof crate); *library* = a library crate (`data`, the GUMBO library "
           "crate, `firewall-core`, `mavlink_parser_vest`, and the third-party `vest_lib`), measured while "
           "verifying one crate that depends on it.",
           "- **Verified**: number of functions Verus verified in the crate (its `verification results:: N verified`).",
           "- **Errors**: number of verification errors.",
           "- **Verus total (ms)**: median over the runs of Verus' reported `total-time` for the crate: parsing, type "
           "checking, VIR generation, SMT solving and lifetime checking. Cargo's compilation of dependencies is not "
           "included.",
           "- **SMT CPU time (ms)**: median of the time Z3 spent discharging the crate's verification conditions "
           "(Verus' `total smt-run`), *summed over Verus' parallel solver threads* (up to 15 here). It is CPU time, not "
           "elapsed time, so it can exceed Verus total (e.g. `vest_lib`).",
           "- **Runs**: number of measured runs.",
           "- **CV total / CV SMT**: coefficient of variation (standard deviation / mean) of Verus total and SMT CPU "
           "time over the runs. Verus reports times in whole milliseconds, so for SMT times of a few milliseconds a "
           "large CV is rounding, not variability.",
           "- **Throttled runs**: runs before or after which macOS reported a thermal state other than nominal "
           "(`ProcessInfo.thermalState`). Per-run CPU temperature, fan speed and peak P-cluster frequency (from "
           "`macmon`, sampled every 100 ms) are in `verus_timing.csv`.",
           "",
           f"**Method.** Every crate was first verified once (vstd and dependencies verified and cached; one shared "
           f"Cargo target directory per case study; case studies warmed up in parallel), followed by a cool-down of at "
           f"least {WARM_COOL_MIN} s until the CPU was within {WARM_COOL_DT:.0f} C of its idle temperature, the thermal "
           f"state nominal and the fans stopped. Then {runs} rounds, each re-verifying every crate once in turn: only the "
           "crate's own Cargo fingerprint (and, for a library, the library's) is removed and `make verus` (`make all` "
           "for the system-proof crate) is rerun with Verus' `--time`. Each measured run is preceded by a cool-down of "
           f"at least {RUN_COOL_MIN} s until the CPU is within {RUN_COOL_DT:.0f} C of idle and the thermal state nominal. "
           "Cargo runs one job at a time (`CARGO_BUILD_JOBS=1`); Verus itself uses all its threads.",
           "",
           "**Settings.** The generated Makefiles' `SMT_OPTS` (`--rlimit 100 --smt-option smt.random_seed=7`). "
           "Exceptions: the RTS instrumentation mock also uses `CARGO_VERUS_OPTS=\"--fwd-verus-args-to roots\"` and "
           "`--smt-option smt.relevancy=0` (see `rts/readme.md`); Open Platform's ethernet driver is verified with "
           "`MICROKIT_BOARD=qemu_virt_aarch64`.",
           "", "</details>", ""]

    # variability analysis
    worst.sort(reverse=True)
    noisy = [(ct, case, name, med) for ct, case, name, med in worst if ct > 0.05 and med >= 100]
    thr_total = sum(a["thr"] for a in agg.values())
    md += ["## Variability and number of runs", ""]
    if failed:
        md.append(f"Not measured (warm-up failed): {', '.join(f'{c} {p}' for c, p in failed)}.\n")
    md.append(f"{thr_total} measured run(s) were flagged as possibly throttled.")
    if noisy:
        md.append(f"{len(noisy)} crate(s) have a coefficient of variation of Verus total time above 5% (crates whose "
                  "median is under 100 ms are not considered: their absolute variation is negligible):\n")
        md += ["| Case study | Crate | Median total (ms) | CV total | Runs for +-5% (95% CI) |", "|:--|:--|--:|--:|--:|"]
        md += [f"| {case} | `{name}` | {med:.0f} | {ct:.1%} | {runs_needed(ct)} |" for ct, case, name, med in noisy]
        need = max(runs_needed(ct) for ct, *_ in noisy)
        md.append(f"\n**Recommendation:** more runs are warranted; {need} runs would bring every listed crate's 95% "
                  f"confidence interval of the mean within +-5% (currently {runs}).")
    else:
        top = ", ".join(f"`{n}` {ct:.1%}" for ct, _, n, _ in worst[:3])
        md.append(f"No crate with a median of at least 100 ms has a coefficient of variation above 5% (largest: {top}). "
                  f"**Recommendation:** {runs} runs are sufficient; more runs would not change the medians materially.")
    md += ["", "<details>", "<summary>Key</summary>", "",
           "- **Median total (ms)**: median Verus total time of the crate.",
           "- **CV total**: coefficient of variation of its Verus total time.",
           "- **Runs for +-5% (95% CI)**: runs needed for the 95% confidence interval of the mean Verus total time to "
           "be within +-5% of the mean, assuming normally distributed times: ceil((1.96 * CV / 0.05)^2).",
           "", "</details>", ""]
    open(os.path.join(mdir, "verus_timing.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
