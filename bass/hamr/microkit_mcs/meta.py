# Copyright 2025, UNSW
# SPDX-License-Identifier: BSD-2-Clause
import argparse
import struct
from random import randint
from dataclasses import dataclass
from typing import List, Tuple, Optional
from sdfgen import SystemDescription, Sddf, DeviceTree, LionsOs
from importlib.metadata import version

# This file will not be overwritten if HAMR codegen is rerun

assert int(version('sdfgen').split(".")[1]) >= 30, f"Requires sdfgen >= 0.30, found {version('sdfgen')}"

from sdfgen_helper import *

ProtectionDomain = SystemDescription.ProtectionDomain
MemoryRegion = SystemDescription.MemoryRegion
Map = SystemDescription.Map
Channel = SystemDescription.Channel
IrqConventional = SystemDescription.IrqConventional
VirtualMachine = SystemDescription.VirtualMachine

@dataclass
class Board:
    name: str
    arch: SystemDescription.Arch
    paddr_top: int
    serial: str
    timer: str
    ethernet: str
    i2c: Optional[str]


BOARDS: List[Board] = [
    Board(
        name="qemu_virt_aarch64",
        arch=SystemDescription.Arch.AARCH64,
        paddr_top=0x6_0000_000,
        serial="pl011@9000000",
        timer="timer",
        ethernet="virtio_mmio@a003e00",
        i2c=None,
    ),
]

def schedule(*entries):
    """
    entries: sequence of (channel, timeslice_ns)
    """
    part_ch, part_timeslices, is_user_partition = zip(*entries)
    return UserSchedule(list(part_timeslices), list(part_ch), list(is_user_partition))

def generate(sdf_path: str, output_dir: str, dtb: DeviceTree):
    timer_node = dtb.node(board.timer)
    assert timer_node is not None

    timer_driver = ProtectionDomain("timer_driver", "timer_driver.elf", priority=201)
    timer_system = Sddf.Timer(sdf, timer_node, timer_driver)

    scheduler = ProtectionDomain("scheduler", "scheduler.elf", priority=200)


    # BEGIN META MARKER

    #######################################
    # PARTITION PROTECTION DOMAINS
    #######################################
    ArduPilot_ArduPilot_MON = ProtectionDomain(
      name="ArduPilot_ArduPilot_MON",
      program_image="ArduPilot_ArduPilot_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(ArduPilot_ArduPilot_MON)

    ArduPilot_ArduPilot = ProtectionDomain(
      name="ArduPilot_ArduPilot",
      program_image="ArduPilot_ArduPilot.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    ArduPilot_ArduPilot_MON.add_child_pd(ArduPilot_ArduPilot, child_id=1)

    FirewallRx_FirewallRx_MON = ProtectionDomain(
      name="FirewallRx_FirewallRx_MON",
      program_image="FirewallRx_FirewallRx_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(FirewallRx_FirewallRx_MON)

    FirewallRx_FirewallRx = ProtectionDomain(
      name="FirewallRx_FirewallRx",
      program_image="FirewallRx_FirewallRx.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    FirewallRx_FirewallRx_MON.add_child_pd(FirewallRx_FirewallRx, child_id=1)

    FirewallTx_FirewallTx_MON = ProtectionDomain(
      name="FirewallTx_FirewallTx_MON",
      program_image="FirewallTx_FirewallTx_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(FirewallTx_FirewallTx_MON)

    FirewallTx_FirewallTx = ProtectionDomain(
      name="FirewallTx_FirewallTx",
      program_image="FirewallTx_FirewallTx.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    FirewallTx_FirewallTx_MON.add_child_pd(FirewallTx_FirewallTx, child_id=1)

    LowLevelEthernetDriver_LowLevelEthernetDriver_MON = ProtectionDomain(
      name="LowLevelEthernetDriver_LowLevelEthernetDriver_MON",
      program_image="LowLevelEthernetDriver_LowLevelEthernetDriver_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(LowLevelEthernetDriver_LowLevelEthernetDriver_MON)

    LowLevelEthernetDriver_LowLevelEthernetDriver = ProtectionDomain(
      name="LowLevelEthernetDriver_LowLevelEthernetDriver",
      program_image="LowLevelEthernetDriver_LowLevelEthernetDriver.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    LowLevelEthernetDriver_LowLevelEthernetDriver_MON.add_child_pd(LowLevelEthernetDriver_LowLevelEthernetDriver, child_id=1)

    ModeManager_ModeManager_MON = ProtectionDomain(
      name="ModeManager_ModeManager_MON",
      program_image="ModeManager_ModeManager_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(ModeManager_ModeManager_MON)

    ModeManager_ModeManager = ProtectionDomain(
      name="ModeManager_ModeManager",
      program_image="ModeManager_ModeManager.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    ModeManager_ModeManager_MON.add_child_pd(ModeManager_ModeManager, child_id=1)


    #######################################
    # MEMORY REGIONS
    #######################################
    seL4_i_Instance_ArduPilot_ArduPilot_EthernetFramesTx_1_Memory_Region = MemoryRegion(sdf, "seL4_i_Instance_ArduPilot_ArduPilot_EthernetFramesTx_1_Memory_Region", 0x1_000)
    sdf.add_mr(seL4_i_Instance_ArduPilot_ArduPilot_EthernetFramesTx_1_Memory_Region)
    seL4_i_Instance_FirewallRx_FirewallRx_EthernetFramesRxOut_1_Memory_Region = MemoryRegion(sdf, "seL4_i_Instance_FirewallRx_FirewallRx_EthernetFramesRxOut_1_Memory_Region", 0x1_000)
    sdf.add_mr(seL4_i_Instance_FirewallRx_FirewallRx_EthernetFramesRxOut_1_Memory_Region)
    seL4_i_Instance_FirewallRx_FirewallRx_AttackStatusRx_1_Memory_Region = MemoryRegion(sdf, "seL4_i_Instance_FirewallRx_FirewallRx_AttackStatusRx_1_Memory_Region", 0x1_000)
    sdf.add_mr(seL4_i_Instance_FirewallRx_FirewallRx_AttackStatusRx_1_Memory_Region)
    seL4_i_Instance_FirewallTx_FirewallTx_EthernetFramesTxOut_1_Memory_Region = MemoryRegion(sdf, "seL4_i_Instance_FirewallTx_FirewallTx_EthernetFramesTxOut_1_Memory_Region", 0x1_000)
    sdf.add_mr(seL4_i_Instance_FirewallTx_FirewallTx_EthernetFramesTxOut_1_Memory_Region)
    seL4_i_Instance_FirewallTx_FirewallTx_AttackStatusTx_1_Memory_Region = MemoryRegion(sdf, "seL4_i_Instance_FirewallTx_FirewallTx_AttackStatusTx_1_Memory_Region", 0x1_000)
    sdf.add_mr(seL4_i_Instance_FirewallTx_FirewallTx_AttackStatusTx_1_Memory_Region)
    seL4_i_Instance_LowLevelEthernetDriver_LowLevelEthernetDriver_EthernetFramesRx_1_Memory_Region = MemoryRegion(sdf, "seL4_i_Instance_LowLevelEthernetDriver_LowLevelEthernetDriver_EthernetFramesRx_1_Memory_Region", 0x1_000)
    sdf.add_mr(seL4_i_Instance_LowLevelEthernetDriver_LowLevelEthernetDriver_EthernetFramesRx_1_Memory_Region)
    seL4_i_Instance_ModeManager_ModeManager_CurrentMode_1_Memory_Region = MemoryRegion(sdf, "seL4_i_Instance_ModeManager_ModeManager_CurrentMode_1_Memory_Region", 0x1_000)
    sdf.add_mr(seL4_i_Instance_ModeManager_ModeManager_CurrentMode_1_Memory_Region)

    ArduPilot_ArduPilot.add_map(Map(seL4_i_Instance_ArduPilot_ArduPilot_EthernetFramesTx_1_Memory_Region, 0x10_000_000, perms="rw", setvar_vaddr="EthernetFramesTx_queue_1"))
    FirewallTx_FirewallTx.add_map(Map(seL4_i_Instance_ArduPilot_ArduPilot_EthernetFramesTx_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="EthernetFramesTxIn_queue_1"))
    ArduPilot_ArduPilot.add_map(Map(seL4_i_Instance_FirewallRx_FirewallRx_EthernetFramesRxOut_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="EthernetFramesRx_queue_1"))
    FirewallRx_FirewallRx.add_map(Map(seL4_i_Instance_FirewallRx_FirewallRx_EthernetFramesRxOut_1_Memory_Region, 0x10_000_000, perms="rw", setvar_vaddr="EthernetFramesRxOut_queue_1"))
    FirewallRx_FirewallRx.add_map(Map(seL4_i_Instance_FirewallRx_FirewallRx_AttackStatusRx_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="AttackStatusRx_queue_1"))
    ModeManager_ModeManager.add_map(Map(seL4_i_Instance_FirewallRx_FirewallRx_AttackStatusRx_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="AttackStatusRx_queue_1"))
    FirewallTx_FirewallTx.add_map(Map(seL4_i_Instance_FirewallTx_FirewallTx_EthernetFramesTxOut_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="EthernetFramesTxOut_queue_1"))
    LowLevelEthernetDriver_LowLevelEthernetDriver.add_map(Map(seL4_i_Instance_FirewallTx_FirewallTx_EthernetFramesTxOut_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="EthernetFramesTx_queue_1"))
    FirewallTx_FirewallTx.add_map(Map(seL4_i_Instance_FirewallTx_FirewallTx_AttackStatusTx_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="AttackStatusTx_queue_1"))
    ModeManager_ModeManager.add_map(Map(seL4_i_Instance_FirewallTx_FirewallTx_AttackStatusTx_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="AttackStatusTx_queue_1"))
    FirewallRx_FirewallRx.add_map(Map(seL4_i_Instance_LowLevelEthernetDriver_LowLevelEthernetDriver_EthernetFramesRx_1_Memory_Region, 0x10_004_000, perms="r", setvar_vaddr="EthernetFramesRxIn_queue_1"))
    LowLevelEthernetDriver_LowLevelEthernetDriver.add_map(Map(seL4_i_Instance_LowLevelEthernetDriver_LowLevelEthernetDriver_EthernetFramesRx_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="EthernetFramesRx_queue_1"))
    FirewallRx_FirewallRx.add_map(Map(seL4_i_Instance_ModeManager_ModeManager_CurrentMode_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="CurrentMode_queue_1"))
    FirewallTx_FirewallTx.add_map(Map(seL4_i_Instance_ModeManager_ModeManager_CurrentMode_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="CurrentMode_queue_1"))
    ModeManager_ModeManager.add_map(Map(seL4_i_Instance_ModeManager_ModeManager_CurrentMode_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="CurrentMode_queue_1"))



    #######################################
    # CHANNELS
    #######################################
    channel_ArduPilot_ArduPilot_MON = 5
    channel_FirewallRx_FirewallRx_MON = 3
    channel_FirewallTx_FirewallTx_MON = 4
    channel_LowLevelEthernetDriver_LowLevelEthernetDriver_MON = 2
    channel_ModeManager_ModeManager_MON = 6

    sdf.add_channel(Channel(a=scheduler, a_id=5, b=ArduPilot_ArduPilot_MON, b_id=0))
    sdf.add_channel(Channel(a=ArduPilot_ArduPilot_MON, a_id=1, b=ArduPilot_ArduPilot, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=3, b=FirewallRx_FirewallRx_MON, b_id=0))
    sdf.add_channel(Channel(a=FirewallRx_FirewallRx_MON, a_id=1, b=FirewallRx_FirewallRx, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=4, b=FirewallTx_FirewallTx_MON, b_id=0))
    sdf.add_channel(Channel(a=FirewallTx_FirewallTx_MON, a_id=1, b=FirewallTx_FirewallTx, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=2, b=LowLevelEthernetDriver_LowLevelEthernetDriver_MON, b_id=0))
    sdf.add_channel(Channel(a=LowLevelEthernetDriver_LowLevelEthernetDriver_MON, a_id=1, b=LowLevelEthernetDriver_LowLevelEthernetDriver, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=6, b=ModeManager_ModeManager_MON, b_id=0))
    sdf.add_channel(Channel(a=ModeManager_ModeManager_MON, a_id=1, b=ModeManager_ModeManager, b_id=0))

    #######################################
    # SCHEDULE
    #######################################
    ts_LowLevelEthernetDriver_LowLevelEthernetDriver_MON = (channel_LowLevelEthernetDriver_LowLevelEthernetDriver_MON, 100000000, True)
    ts_FirewallRx_FirewallRx_MON = (channel_FirewallRx_FirewallRx_MON, 100000000, True)
    ts_FirewallTx_FirewallTx_MON = (channel_FirewallTx_FirewallTx_MON, 100000000, True)
    ts_ArduPilot_ArduPilot_MON = (channel_ArduPilot_ArduPilot_MON, 100000000, True)
    ts_ModeManager_ModeManager_MON = (channel_ModeManager_ModeManager_MON, 100000000, True)
    ts_pad = (0, 500000000, False)

    user_schedule = schedule(
      ts_LowLevelEthernetDriver_LowLevelEthernetDriver_MON,
      ts_FirewallRx_FirewallRx_MON,
      ts_FirewallTx_FirewallTx_MON,
      ts_ArduPilot_ArduPilot_MON,
      ts_ModeManager_ModeManager_MON,
      ts_pad
    )

    # END META MARKER

    sdf.add_pd(timer_driver)
    sdf.add_pd(scheduler)
    timer_system.add_client(scheduler)

    assert timer_system.connect()
    assert timer_system.serialise_config(output_dir)

    data_path = output_dir + "/schedule_config.data"
    with open(data_path, "wb+") as f:
        f.write(user_schedule.serialise())
    update_elf_section(obj_copy, scheduler.program_image,
                       user_schedule.section_name,
                       data_path)

    with open(f"{output_dir}/{sdf_path}", "w+") as f:
        f.write(sdf.render())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dtb", required=True)
    parser.add_argument("--sddf", required=True)
    parser.add_argument("--board", required=True, choices=[b.name for b in BOARDS])
    parser.add_argument("--output", required=True)
    parser.add_argument("--sdf", required=True)
    parser.add_argument("--objcopy", required=True)
    # Substring filter selecting which system tests to run; empty means all of
    # them.  Only the test scheduler variant consumes it.
    parser.add_argument("--tests", required=False, default="")

    args = parser.parse_args()

    # Import the config structs module from the build directory
    sys.path.append(args.output)
    from config_structs import *

    board = next(filter(lambda b: b.name == args.board, BOARDS))

    sdf = SystemDescription(board.arch, board.paddr_top)
    sddf = Sddf(args.sddf)

    global obj_copy
    obj_copy = args.objcopy

    global tests_filter
    tests_filter = args.tests

    with open(args.dtb, "rb") as f:
        dtb = DeviceTree(f.read())

    generate(args.sdf, args.output, dtb)
