::#! 2> /dev/null                                   #
@ 2>/dev/null # 2>nul & echo off & goto BOF         #
if [ -z ${SIREUM_HOME} ]; then                      #
  echo "Please set SIREUM_HOME env var"             #
  exit -1                                           #
fi                                                  #
exec ${SIREUM_HOME}/bin/sireum slang run "$0" "$@"  #
:BOF
setlocal
if not defined SIREUM_HOME (
  echo Please set SIREUM_HOME env var
  exit /B -1
)
%SIREUM_HOME%\\bin\\sireum.bat slang run "%0" %*
exit /B %errorlevel%
::!#
// #Sireum

// Removes HAMR-generated files so that rerunning codegen (bin/run-hamr.cmd)
// recreates them from the current HAMR templates (e.g. to pick up new Verus/Rust
// versions in a crate's Cargo.toml / rust-toolchain.toml). Files containing
// "Do not edit" are always removed; any other file is removed unless it matches
// toKeep below, which lists the developer-supplied and developer-modified files.

import org.sireum._

val hamrDir: Os.Path = Os.slashDir.up.up / "hamr"
val microkitMcsDir = hamrDir / "microkit_mcs"

assert (hamrDir.exists, hamrDir.value)

@sig trait Keep {
  @pure def keep(f: Os.Path): B
}
@datatype class KeepPath (path: Os.Path) extends Keep {
  @pure def keep(f: Os.Path): B = {
    return f == path
  }
}
@datatype class KeepPattern (pattern: String) extends Keep {
  @pure def keep(f: Os.Path): B = {
    return ops.StringOps(f.value).contains(pattern)
  }
}

val crates = microkitMcsDir / "crates"
val ardupilot = microkitMcsDir / "components" / "seL4_ArduPilot_ArduPilot"
val ethDriver = "seL4_LowLevelEthernetDriver_LowLevelEthernetDriver"

val toKeep = ISZ(
  KeepPattern(".gitignore"),
  KeepPattern(".idea"),
  KeepPattern("clean.cmd"),
  KeepPattern("run-hamr.cmd"),
  KeepPattern("run-logika.cmd"),

  KeepPattern(".md"), // readmes

  KeepPattern("_user.c"), // microkit C user implementation file
  KeepPattern("_user.h"), // microkit C user header (VM IRQ configuration)

  KeepPattern("_app.rs"), // microkit Rust user implementation files
  KeepPattern("_app/"), // user modules of the Rust implementations (e.g. config.rs)

  KeepPattern("src/test/mod.rs"), // keep any user additions
  KeepPattern("tests.rs"), // any file ending in tests.rs

  // codegen will weave in autogen code to files that have inverted markers
  KeepPattern("microkit.schedule.xml"),
  KeepPattern("microkit.system"),

  // ---- Open Platform developer-supplied code and build configuration ----

  // library crates written by the developers
  KeepPath(crates / "firewall_core"),
  KeepPath(crates / "mavlink_parser_vest"),
  KeepPath(crates / ethDriver / "core"), // ZCU102 GEM ethernet driver

  // crate manifests the developers extended with dependencies on the crates above
  // (firewall-core, mavlink_parser_vest, the eth driver core / rust-sel4 crates)
  KeepPath(crates / ethDriver / "Cargo.toml"),
  KeepPath(crates / ethDriver / "Makefile"), // selects the qemu-virtio/zcu102 driver feature
  KeepPath(crates / "seL4_MavlinkFirewall_MavlinkFirewall" / "Cargo.toml"),
  KeepPath(crates / "seL4_RxFirewall_RxFirewall" / "Cargo.toml"),
  KeepPath(crates / "seL4_TxFirewall_TxFirewall" / "Cargo.toml"),

  // ArduPilot VM: board configurations (QEMU and ZCU102) and virtio support
  KeepPath(ardupilot / "board"),
  KeepPath(ardupilot / "src" / "virtio"),
  KeepPattern("qemu_virtio_net_client.c"), // QEMU virtio-net backend for the ethernet driver

  // QEMU / ZCU102 build and system-description configuration
  KeepPath(microkitMcsDir / "meta.py"),
  KeepPattern(".mk"), // qemu.mk, zcu102.mk, ... (HAMR's system.mk is "Do not edit" so still removed)
  KeepPath(microkitMcsDir / "Dockerfile"),
  KeepPath(microkitMcsDir / "docker_compose.yml"),
)

@pure def keep(f: Os.Path): B = {
  for (p <- toKeep if p.keep(f)) {
    return T
  }
  return F
}

def rec(p: Os.Path, onlyDelAutoGen: B): Unit = {
  if(p.isFile) {
    if ((!keep(p) && !onlyDelAutoGen) || ops.StringOps(p.read).contains("Do not edit")) {
      p.remove()
      println(s"Removed file: $p")
    }
  } else {
    for (pp <- p.list) {
      rec(pp, keep(p) || onlyDelAutoGen)
    }
    if (p.list.isEmpty) {
      p.removeAll()
      println(s"Removed empty directory: $p")
    }
  }
}

if (Os.cliArgs.nonEmpty) {
  for (a <- Os.cliArgs) {
    val d = Os.path(a)
    assert (d.exists, s"$d is not a valid directory")
    rec(d, F)
  }
} else if (microkitMcsDir.exists) {
  rec(microkitMcsDir, F)
}
