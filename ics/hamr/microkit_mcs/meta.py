# Copyright 2025, UNSW
# SPDX-License-Identifier: BSD-2-Clause
import argparse
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List, Optional
from sdfgen import SystemDescription, Sddf, DeviceTree
from importlib.metadata import version

# This file will not be overwritten if HAMR codegen is rerun

assert int(version('sdfgen').split(".")[1]) >= 30, \
    f"Requires sdfgen >= 0.30, found {version('sdfgen')}"

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
    ethernet: Optional[str]
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
    Board(
        name="rpi4b_4gb",
        arch=SystemDescription.Arch.AARCH64,
        paddr_top=0x2_000_000,
        serial="soc/serial@7e215040",
        timer="soc/timer@7e003000",
        ethernet=None,
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
    cpuSw_wifiDriver_wifiDriver_wifiDriver_MON = ProtectionDomain(
      name="cpuSw_wifiDriver_wifiDriver_wifiDriver_MON",
      program_image="cpuSw_wifiDriver_wifiDriver_wifiDriver_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_wifiDriver_wifiDriver_wifiDriver_MON)

    cpuSw_wifiDriver_wifiDriver_wifiDriver = ProtectionDomain(
      name="cpuSw_wifiDriver_wifiDriver_wifiDriver",
      program_image="cpuSw_wifiDriver_wifiDriver_wifiDriver.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_wifiDriver_wifiDriver_wifiDriver_MON.add_child_pd(cpuSw_wifiDriver_wifiDriver_wifiDriver, child_id=1)

    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON = ProtectionDomain(
      name="cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON",
      program_image="cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON)

    cpuSw_wifiDriver_wifiDriverVM_wifiDriver = ProtectionDomain(
      name="cpuSw_wifiDriver_wifiDriverVM_wifiDriver",
      program_image="cpuSw_wifiDriver_wifiDriverVM_wifiDriver.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON.add_child_pd(cpuSw_wifiDriver_wifiDriverVM_wifiDriver, child_id=1)
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_irq(IrqConventional(irq=33, id=1))
    cpuSw_btDriver_btDriver_MON = ProtectionDomain(
      name="cpuSw_btDriver_btDriver_MON",
      program_image="cpuSw_btDriver_btDriver_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_btDriver_btDriver_MON)

    cpuSw_btDriver_btDriver = ProtectionDomain(
      name="cpuSw_btDriver_btDriver",
      program_image="cpuSw_btDriver_btDriver.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_btDriver_btDriver_MON.add_child_pd(cpuSw_btDriver_btDriver, child_id=1)

    cpuSw_usbDriver_usbDriver_MON = ProtectionDomain(
      name="cpuSw_usbDriver_usbDriver_MON",
      program_image="cpuSw_usbDriver_usbDriver_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_usbDriver_usbDriver_MON)

    cpuSw_usbDriver_usbDriver = ProtectionDomain(
      name="cpuSw_usbDriver_usbDriver",
      program_image="cpuSw_usbDriver_usbDriver.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_usbDriver_usbDriver_MON.add_child_pd(cpuSw_usbDriver_usbDriver, child_id=1)

    cpuSw_dataManager_dataManager_dataManager_MON = ProtectionDomain(
      name="cpuSw_dataManager_dataManager_dataManager_MON",
      program_image="cpuSw_dataManager_dataManager_dataManager_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_dataManager_dataManager_dataManager_MON)

    cpuSw_dataManager_dataManager_dataManager = ProtectionDomain(
      name="cpuSw_dataManager_dataManager_dataManager",
      program_image="cpuSw_dataManager_dataManager_dataManager.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_dataManager_dataManager_dataManager_MON.add_child_pd(cpuSw_dataManager_dataManager_dataManager, child_id=1)

    cpuSw_dataManager_dataStorage_dataStorage_MON = ProtectionDomain(
      name="cpuSw_dataManager_dataStorage_dataStorage_MON",
      program_image="cpuSw_dataManager_dataStorage_dataStorage_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_dataManager_dataStorage_dataStorage_MON)

    cpuSw_dataManager_dataStorage_dataStorage = ProtectionDomain(
      name="cpuSw_dataManager_dataStorage_dataStorage",
      program_image="cpuSw_dataManager_dataStorage_dataStorage.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_dataManager_dataStorage_dataStorage_MON.add_child_pd(cpuSw_dataManager_dataStorage_dataStorage, child_id=1)
    cpuSw_dataManager_dataStorage_dataStorage.add_irq(IrqConventional(irq=33, id=1))
    cpuSw_dataAnalysis_dataAnalysis_MON = ProtectionDomain(
      name="cpuSw_dataAnalysis_dataAnalysis_MON",
      program_image="cpuSw_dataAnalysis_dataAnalysis_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_dataAnalysis_dataAnalysis_MON)

    cpuSw_dataAnalysis_dataAnalysis = ProtectionDomain(
      name="cpuSw_dataAnalysis_dataAnalysis",
      program_image="cpuSw_dataAnalysis_dataAnalysis.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_dataAnalysis_dataAnalysis_MON.add_child_pd(cpuSw_dataAnalysis_dataAnalysis, child_id=1)

    cpuSw_decryptor_decryptor_MON = ProtectionDomain(
      name="cpuSw_decryptor_decryptor_MON",
      program_image="cpuSw_decryptor_decryptor_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_decryptor_decryptor_MON)

    cpuSw_decryptor_decryptor = ProtectionDomain(
      name="cpuSw_decryptor_decryptor",
      program_image="cpuSw_decryptor_decryptor.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_decryptor_decryptor_MON.add_child_pd(cpuSw_decryptor_decryptor, child_id=1)

    cpuSw_encryptor_encryptor_MON = ProtectionDomain(
      name="cpuSw_encryptor_encryptor_MON",
      program_image="cpuSw_encryptor_encryptor_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_encryptor_encryptor_MON)

    cpuSw_encryptor_encryptor = ProtectionDomain(
      name="cpuSw_encryptor_encryptor",
      program_image="cpuSw_encryptor_encryptor.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_encryptor_encryptor_MON.add_child_pd(cpuSw_encryptor_encryptor, child_id=1)

    cpuSw_logMonitor_logMonitor_MON = ProtectionDomain(
      name="cpuSw_logMonitor_logMonitor_MON",
      program_image="cpuSw_logMonitor_logMonitor_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_logMonitor_logMonitor_MON)

    cpuSw_logMonitor_logMonitor = ProtectionDomain(
      name="cpuSw_logMonitor_logMonitor",
      program_image="cpuSw_logMonitor_logMonitor.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_logMonitor_logMonitor_MON.add_child_pd(cpuSw_logMonitor_logMonitor, child_id=1)

    cpuSw_reportMonitor_reportMonitor_MON = ProtectionDomain(
      name="cpuSw_reportMonitor_reportMonitor_MON",
      program_image="cpuSw_reportMonitor_reportMonitor_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_reportMonitor_reportMonitor_MON)

    cpuSw_reportMonitor_reportMonitor = ProtectionDomain(
      name="cpuSw_reportMonitor_reportMonitor",
      program_image="cpuSw_reportMonitor_reportMonitor.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_reportMonitor_reportMonitor_MON.add_child_pd(cpuSw_reportMonitor_reportMonitor, child_id=1)

    cpuSw_firewall_firewall_MON = ProtectionDomain(
      name="cpuSw_firewall_firewall_MON",
      program_image="cpuSw_firewall_firewall_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(cpuSw_firewall_firewall_MON)

    cpuSw_firewall_firewall = ProtectionDomain(
      name="cpuSw_firewall_firewall",
      program_image="cpuSw_firewall_firewall.elf",
      priority=140,
      passive=True,
      stack_size=0x100_000)
    cpuSw_firewall_firewall_MON.add_child_pd(cpuSw_firewall_firewall, child_id=1)


    #######################################
    # MEMORY REGIONS
    #######################################
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM", 0x10_000_000, paddr=0x40_000_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_GIC = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_GIC", 0x1_000, paddr=0x8_040_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_GIC)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Serial = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Serial", 0x1_000, paddr=0x9_000_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Serial)
    GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Guest_RAM = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Guest_RAM", 0x10_000_000, paddr=0x40_000_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Guest_RAM)
    GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_GIC = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_GIC", 0x1_000, paddr=0x8_040_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_GIC)
    GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Serial = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Serial", 0x1_000, paddr=0x9_000_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Serial)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_wifiSend_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_wifiSend_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_wifiSend_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_HMD_log_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_HMD_log_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_HMD_log_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_analysis_request_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_analysis_request_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_analysis_request_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvOut_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvOut_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvOut_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvIn_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvIn_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvIn_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiSendOut_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiSendOut_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiSendOut_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btRecv_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btRecv_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btRecv_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btSend_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btSend_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btSend_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbRecv_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbRecv_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbRecv_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbSend_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbSend_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbSend_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_encrypted_log_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_encrypted_log_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_encrypted_log_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_storage_request_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_storage_request_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_storage_request_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_response_log_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_response_log_1_Memory_Region", 0x2_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_response_log_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_encrypted_response_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_encrypted_response_1_Memory_Region", 0x15_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_encrypted_response_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_request_log_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_request_log_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_request_log_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_analysis_report_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_analysis_report_1_Memory_Region", 0x2_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_analysis_report_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_decryptor_decryptor_HMD_log_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_decryptor_decryptor_HMD_log_out_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_decryptor_decryptor_HMD_log_out_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_encryptor_encryptor_analysis_report_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_encryptor_encryptor_analysis_report_out_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_encryptor_encryptor_analysis_report_out_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_response_log_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_response_log_out_1_Memory_Region", 0x2_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_response_log_out_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_alert_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_alert_out_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_alert_out_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_storage_alert_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_storage_alert_out_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_storage_alert_out_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_analysis_report_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_analysis_report_out_1_Memory_Region", 0x3_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_analysis_report_out_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_alert_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_alert_out_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_alert_out_1_Memory_Region)
    GroundStation_Impl_Instance_cpuSw_firewall_firewall_analysis_request_out_1_Memory_Region = MemoryRegion(sdf, "GroundStation_Impl_Instance_cpuSw_firewall_firewall_analysis_request_out_1_Memory_Region", 0x1_000)
    sdf.add_mr(GroundStation_Impl_Instance_cpuSw_firewall_firewall_analysis_request_out_1_Memory_Region)

    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM, 0x40_000_000, perms="rw", setvar_vaddr="GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM_vaddr"))
    cpuSw_dataManager_dataStorage_dataStorage.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Guest_RAM, 0x40_000_000, perms="rw", setvar_vaddr="GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Guest_RAM_vaddr"))
    cpuSw_wifiDriver_wifiDriver_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_wifiSend_1_Memory_Region, 0x10_000_000, perms="rw", setvar_vaddr="wifiSend_queue_1"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_wifiSend_1_Memory_Region, 0x20_000_000, perms="r", setvar_vaddr="wifiSendIn_queue_1"))
    cpuSw_wifiDriver_wifiDriver_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_HMD_log_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="HMD_log_queue_1"))
    cpuSw_decryptor_decryptor.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_HMD_log_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="HMD_log_in_queue_1"))
    cpuSw_wifiDriver_wifiDriver_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_analysis_request_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="analysis_request_queue_1"))
    cpuSw_reportMonitor_reportMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_analysis_request_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="analysis_request_queue_1"))
    cpuSw_firewall_firewall.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriver_wifiDriver_analysis_request_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="analysis_request_in_queue_1"))
    cpuSw_wifiDriver_wifiDriver_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvOut_1_Memory_Region, 0x10_00A_000, perms="r", setvar_vaddr="wifiRecv_queue_1"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvOut_1_Memory_Region, 0x20_004_000, perms="rw", setvar_vaddr="wifiRecvOut_queue_1"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiRecvIn_1_Memory_Region, 0x20_008_000, perms="r", setvar_vaddr="wifiRecvIn_queue_1"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_wifiSendOut_1_Memory_Region, 0x20_00C_000, perms="rw", setvar_vaddr="wifiSendOut_queue_1"))
    cpuSw_btDriver_btDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btRecv_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="btRecv_queue_1"))
    cpuSw_btDriver_btDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_btDriver_btDriver_btSend_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="btSend_queue_1"))
    cpuSw_usbDriver_usbDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbRecv_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="usbRecv_queue_1"))
    cpuSw_usbDriver_usbDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_usbDriver_usbDriver_usbSend_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="usbSend_queue_1"))
    cpuSw_dataManager_dataManager_dataManager.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_encrypted_log_1_Memory_Region, 0x10_000_000, perms="rw", setvar_vaddr="encrypted_log_queue_1"))
    cpuSw_dataManager_dataStorage_dataStorage.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_encrypted_log_1_Memory_Region, 0x20_000_000, perms="r", setvar_vaddr="encrypted_log_queue_1"))
    cpuSw_dataManager_dataManager_dataManager.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_storage_request_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="storage_request_queue_1"))
    cpuSw_dataManager_dataStorage_dataStorage.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_storage_request_1_Memory_Region, 0x20_004_000, perms="r", setvar_vaddr="storage_request_queue_1"))
    cpuSw_dataManager_dataManager_dataManager.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_response_log_1_Memory_Region, 0x10_006_000, perms="rw", setvar_vaddr="response_log_queue_1"))
    cpuSw_logMonitor_logMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataManager_dataManager_response_log_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="response_log_in_queue_1"))
    cpuSw_dataManager_dataManager_dataManager.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_encrypted_response_1_Memory_Region, 0x10_009_000, perms="r", setvar_vaddr="encrypted_response_queue_1"))
    cpuSw_dataManager_dataStorage_dataStorage.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_encrypted_response_1_Memory_Region, 0x20_006_000, perms="rw", setvar_vaddr="encrypted_response_queue_1"))
    cpuSw_dataManager_dataManager_dataManager.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_request_log_1_Memory_Region, 0x10_01F_000, perms="r", setvar_vaddr="request_log_queue_1"))
    cpuSw_dataAnalysis_dataAnalysis.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_request_log_1_Memory_Region, 0x10_000_000, perms="rw", setvar_vaddr="request_log_queue_1"))
    cpuSw_logMonitor_logMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_request_log_1_Memory_Region, 0x10_003_000, perms="r", setvar_vaddr="request_log_queue_1"))
    cpuSw_dataAnalysis_dataAnalysis.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_analysis_report_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="analysis_report_queue_1"))
    cpuSw_encryptor_encryptor.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataAnalysis_dataAnalysis_analysis_report_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="analysis_report_in_queue_1"))
    cpuSw_dataManager_dataManager_dataManager.add_map(Map(GroundStation_Impl_Instance_cpuSw_decryptor_decryptor_HMD_log_out_1_Memory_Region, 0x10_021_000, perms="r", setvar_vaddr="HMD_log_queue_1"))
    cpuSw_decryptor_decryptor.add_map(Map(GroundStation_Impl_Instance_cpuSw_decryptor_decryptor_HMD_log_out_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="HMD_log_out_queue_1"))
    cpuSw_encryptor_encryptor.add_map(Map(GroundStation_Impl_Instance_cpuSw_encryptor_encryptor_analysis_report_out_1_Memory_Region, 0x10_003_000, perms="rw", setvar_vaddr="analysis_report_out_queue_1"))
    cpuSw_reportMonitor_reportMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_encryptor_encryptor_analysis_report_out_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="analysis_report_in_queue_1"))
    cpuSw_dataAnalysis_dataAnalysis.add_map(Map(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_response_log_out_1_Memory_Region, 0x10_005_000, perms="r", setvar_vaddr="response_log_queue_1"))
    cpuSw_logMonitor_logMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_response_log_out_1_Memory_Region, 0x10_005_000, perms="rw", setvar_vaddr="response_log_out_queue_1"))
    cpuSw_dataManager_dataManager_dataManager.add_map(Map(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_alert_out_1_Memory_Region, 0x10_023_000, perms="r", setvar_vaddr="zeroize_queue_1"))
    cpuSw_logMonitor_logMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_alert_out_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="alert_out_queue_1"))
    cpuSw_dataManager_dataStorage_dataStorage.add_map(Map(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_storage_alert_out_1_Memory_Region, 0x20_01C_000, perms="r", setvar_vaddr="zeroize_queue_1"))
    cpuSw_logMonitor_logMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_logMonitor_logMonitor_storage_alert_out_1_Memory_Region, 0x10_00A_000, perms="rw", setvar_vaddr="storage_alert_out_queue_1"))
    cpuSw_wifiDriver_wifiDriver_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_analysis_report_out_1_Memory_Region, 0x10_00E_000, perms="r", setvar_vaddr="analysis_report_queue_1"))
    cpuSw_reportMonitor_reportMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_analysis_report_out_1_Memory_Region, 0x10_006_000, perms="rw", setvar_vaddr="analysis_report_out_queue_1"))
    cpuSw_wifiDriver_wifiDriver_wifiDriver.add_map(Map(GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_alert_out_1_Memory_Region, 0x10_012_000, perms="r", setvar_vaddr="alert_in_queue_1"))
    cpuSw_reportMonitor_reportMonitor.add_map(Map(GroundStation_Impl_Instance_cpuSw_reportMonitor_reportMonitor_alert_out_1_Memory_Region, 0x10_00A_000, perms="rw", setvar_vaddr="alert_out_queue_1"))
    cpuSw_dataAnalysis_dataAnalysis.add_map(Map(GroundStation_Impl_Instance_cpuSw_firewall_firewall_analysis_request_out_1_Memory_Region, 0x10_008_000, perms="r", setvar_vaddr="analysis_request_queue_1"))
    cpuSw_firewall_firewall.add_map(Map(GroundStation_Impl_Instance_cpuSw_firewall_firewall_analysis_request_out_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="analysis_request_out_queue_1"))

    #######################################
    # VMMs
    #######################################
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm = VirtualMachine("cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM", [VirtualMachine.Vcpu(id=0)])
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM, 0x40_000_000, perms="rwx"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_GIC, 0x8_010_000, perms="rw", cached=False))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(Map(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Serial, 0x9_000_000, perms="rw", cached=False))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.set_virtual_machine(cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm)
    cpuSw_dataManager_dataStorage_dataStorage_VM_vm = VirtualMachine("cpuSw_dataManager_dataStorage_dataStorage_VM", [VirtualMachine.Vcpu(id=0)])
    cpuSw_dataManager_dataStorage_dataStorage_VM_vm.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Guest_RAM, 0x40_000_000, perms="rwx"))
    cpuSw_dataManager_dataStorage_dataStorage_VM_vm.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_GIC, 0x8_010_000, perms="rw", cached=False))
    cpuSw_dataManager_dataStorage_dataStorage_VM_vm.add_map(Map(GroundStation_Impl_Instance_cpuSw_dataManager_dataStorage_dataStorage_VM_Serial, 0x9_000_000, perms="rw", cached=False))
    cpuSw_dataManager_dataStorage_dataStorage.set_virtual_machine(cpuSw_dataManager_dataStorage_dataStorage_VM_vm)

    #######################################
    # CHANNELS
    #######################################
    channel_cpuSw_wifiDriver_wifiDriver_wifiDriver_MON = 3
    channel_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON = 2
    channel_cpuSw_btDriver_btDriver_MON = 11
    channel_cpuSw_usbDriver_usbDriver_MON = 12
    channel_cpuSw_dataManager_dataManager_dataManager_MON = 7
    channel_cpuSw_dataManager_dataStorage_dataStorage_MON = 13
    channel_cpuSw_dataAnalysis_dataAnalysis_MON = 6
    channel_cpuSw_decryptor_decryptor_MON = 4
    channel_cpuSw_encryptor_encryptor_MON = 9
    channel_cpuSw_logMonitor_logMonitor_MON = 8
    channel_cpuSw_reportMonitor_reportMonitor_MON = 10
    channel_cpuSw_firewall_firewall_MON = 5

    sdf.add_channel(Channel(a=scheduler, a_id=3, b=cpuSw_wifiDriver_wifiDriver_wifiDriver_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_wifiDriver_wifiDriver_wifiDriver_MON, a_id=1, b=cpuSw_wifiDriver_wifiDriver_wifiDriver, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=2, b=cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON, a_id=1, b=cpuSw_wifiDriver_wifiDriverVM_wifiDriver, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=11, b=cpuSw_btDriver_btDriver_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_btDriver_btDriver_MON, a_id=1, b=cpuSw_btDriver_btDriver, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=12, b=cpuSw_usbDriver_usbDriver_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_usbDriver_usbDriver_MON, a_id=1, b=cpuSw_usbDriver_usbDriver, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=7, b=cpuSw_dataManager_dataManager_dataManager_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_dataManager_dataManager_dataManager_MON, a_id=1, b=cpuSw_dataManager_dataManager_dataManager, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=13, b=cpuSw_dataManager_dataStorage_dataStorage_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_dataManager_dataStorage_dataStorage_MON, a_id=1, b=cpuSw_dataManager_dataStorage_dataStorage, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=6, b=cpuSw_dataAnalysis_dataAnalysis_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_dataAnalysis_dataAnalysis_MON, a_id=1, b=cpuSw_dataAnalysis_dataAnalysis, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=4, b=cpuSw_decryptor_decryptor_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_decryptor_decryptor_MON, a_id=1, b=cpuSw_decryptor_decryptor, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=9, b=cpuSw_encryptor_encryptor_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_encryptor_encryptor_MON, a_id=1, b=cpuSw_encryptor_encryptor, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=8, b=cpuSw_logMonitor_logMonitor_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_logMonitor_logMonitor_MON, a_id=1, b=cpuSw_logMonitor_logMonitor, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=10, b=cpuSw_reportMonitor_reportMonitor_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_reportMonitor_reportMonitor_MON, a_id=1, b=cpuSw_reportMonitor_reportMonitor, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=5, b=cpuSw_firewall_firewall_MON, b_id=0))
    sdf.add_channel(Channel(a=cpuSw_firewall_firewall_MON, a_id=1, b=cpuSw_firewall_firewall, b_id=0))

    #######################################
    # SCHEDULE
    #######################################
    ts_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON = (channel_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON, 150000000, True)
    ts_cpuSw_wifiDriver_wifiDriver_wifiDriver_MON = (channel_cpuSw_wifiDriver_wifiDriver_wifiDriver_MON, 50000000, True)
    ts_cpuSw_decryptor_decryptor_MON = (channel_cpuSw_decryptor_decryptor_MON, 50000000, True)
    ts_cpuSw_firewall_firewall_MON = (channel_cpuSw_firewall_firewall_MON, 50000000, True)
    ts_cpuSw_dataAnalysis_dataAnalysis_MON = (channel_cpuSw_dataAnalysis_dataAnalysis_MON, 50000000, True)
    ts_cpuSw_dataManager_dataManager_dataManager_MON = (channel_cpuSw_dataManager_dataManager_dataManager_MON, 50000000, True)
    ts_cpuSw_logMonitor_logMonitor_MON = (channel_cpuSw_logMonitor_logMonitor_MON, 50000000, True)
    ts_cpuSw_encryptor_encryptor_MON = (channel_cpuSw_encryptor_encryptor_MON, 50000000, True)
    ts_cpuSw_reportMonitor_reportMonitor_MON = (channel_cpuSw_reportMonitor_reportMonitor_MON, 50000000, True)
    ts_cpuSw_btDriver_btDriver_MON = (channel_cpuSw_btDriver_btDriver_MON, 50000000, True)
    ts_cpuSw_usbDriver_usbDriver_MON = (channel_cpuSw_usbDriver_usbDriver_MON, 50000000, True)
    ts_cpuSw_dataManager_dataStorage_dataStorage_MON = (channel_cpuSw_dataManager_dataStorage_dataStorage_MON, 50000000, True)
    ts_pad = (0, 300000000, False)

    user_schedule = schedule(
      ts_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_MON,
      ts_cpuSw_wifiDriver_wifiDriver_wifiDriver_MON,
      ts_cpuSw_decryptor_decryptor_MON,
      ts_cpuSw_firewall_firewall_MON,
      ts_cpuSw_dataAnalysis_dataAnalysis_MON,
      ts_cpuSw_dataManager_dataManager_dataManager_MON,
      ts_cpuSw_logMonitor_logMonitor_MON,
      ts_cpuSw_encryptor_encryptor_MON,
      ts_cpuSw_reportMonitor_reportMonitor_MON,
      ts_cpuSw_btDriver_btDriver_MON,
      ts_cpuSw_usbDriver_usbDriver_MON,
      ts_cpuSw_dataManager_dataStorage_dataStorage_MON,
      ts_pad
    )

    # END META MARKER

    if board.name == "qemu_virt_aarch64":
        RAM = 0x4000_0000
        RAM_SIZE = 0x1000_0000
        GIC_VM = 0x8_010_000
        GIC_VMM = 0x8_040_000
        Serial = 0x9_000_000
        Serial_IRQ = 33
        Internet = 0xA_003_000
        Internet_IRQ = 79
        RX_Buffer = 0x50_000_000
        TX_Buffer = 0x50_002_000
    elif board.name == "rpi4b_4gb":
        RAM = 0x2000_0000
        RAM_SIZE = 0x4000_0000
        GIC_VM = 0xFF84_2000  # CPU interface
        GIC_VMM = 0xFF84_6000  # vCPU interface
        Serial = 0xFE21_5000
        Serial_IRQ = 125
        Internet = 0xFE30_0000
        Internet_IRQ = 158
        RX_Buffer = 0x60_000_000
        TX_Buffer = 0x60_002_000
    else:
        assert False

    wifi_vmm_prefix = \
        "GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_"

    wifi_internet = MemoryRegion(
        sdf, wifi_vmm_prefix + "Guest_Internet", 0x1_000, paddr=Internet)
    wifi_rx_buffer = MemoryRegion(
        sdf, wifi_vmm_prefix + "Guest_RX_Buffer", 0x2_000,
        paddr=RX_Buffer)
    wifi_tx_buffer = MemoryRegion(
        sdf, wifi_vmm_prefix + "Guest_TX_Buffer", 0x2_000,
        paddr=TX_Buffer)
    sdf.add_mr(wifi_internet)
    sdf.add_mr(wifi_rx_buffer)
    sdf.add_mr(wifi_tx_buffer)

    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_map(Map(
        wifi_rx_buffer, RX_Buffer, perms="rw",
        setvar_vaddr=wifi_vmm_prefix + "Guest_RX_Buffer_vaddr"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver.add_map(Map(
        wifi_tx_buffer, TX_Buffer, perms="rw",
        setvar_vaddr=wifi_vmm_prefix + "Guest_TX_Buffer_vaddr"))

    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(
        Map(wifi_rx_buffer, RX_Buffer, perms="rw"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(
        Map(wifi_tx_buffer, TX_Buffer, perms="rw"))
    cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(
        Map(wifi_internet, Internet, perms="rw", cached=False))

    if board.name == "rpi4b_4gb":
        clock_manager = MemoryRegion(
            sdf, wifi_vmm_prefix + "Guest_Clock_Manager", 0x2_000,
            paddr=0xFE10_1000)
        gpio = MemoryRegion(
            sdf, wifi_vmm_prefix + "Guest_GPIO", 0x1_000,
            paddr=0xFE20_0000)
        mailbox = MemoryRegion(
            sdf, wifi_vmm_prefix + "Guest_Mailbox", 0x2_000,
            paddr=0xFE00_B000)
        rng = MemoryRegion(
            sdf, wifi_vmm_prefix + "Guest_Rng", 0x1_000,
            paddr=0xFE10_4000)

        for region in (clock_manager, gpio, mailbox, rng):
            sdf.add_mr(region)
        cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(
            Map(clock_manager, 0xFE10_1000, perms="rw", cached=False))
        cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(
            Map(gpio, 0xFE20_0000, perms="rw", cached=False))
        cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(
            Map(mailbox, 0xFE00_B000, perms="rw", cached=False))
        cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_vm.add_map(
            Map(rng, 0xFE10_4000, perms="rw", cached=False))

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

    # Apply board-specific Wi-Fi VMM settings after the HAMR-generated
    # section. HAMR's model has one set of physical addresses, while the
    # RPi4B and QEMU platforms require different guest RAM, GIC, serial, and
    # interrupt configurations.
    def apply_platform_overrides(xml_str):
        root = ET.fromstring(xml_str)

        def require_one(elements, description):
            matches = list(elements)
            assert len(matches) == 1, \
                f"Expected one {description}, found {len(matches)}"
            return matches[0]

        def memory_region(name):
            return require_one(
                (mr for mr in root.iter('memory_region')
                 if mr.get('name') == name),
                f"memory region named {name}")

        def mapping(parent, region_name):
            return require_one(
                (m for m in parent.findall('map')
                 if m.get('mr') == region_name),
                f"mapping for {region_name}")

        guest_ram_name = wifi_vmm_prefix + "Guest_RAM"
        gic_name = wifi_vmm_prefix + "GIC"
        serial_name = wifi_vmm_prefix + "Serial"

        guest_ram = memory_region(guest_ram_name)
        guest_ram.set('size', hex(RAM_SIZE))
        guest_ram.set('phys_addr', hex(RAM))
        memory_region(gic_name).set('phys_addr', hex(GIC_VMM))
        memory_region(serial_name).set('phys_addr', hex(Serial))

        wifi_pd = require_one(
            (pd for pd in root.iter('protection_domain')
             if pd.get('name') ==
             'cpuSw_wifiDriver_wifiDriverVM_wifiDriver'),
            "Wi-Fi VMM protection domain")
        mapping(wifi_pd, guest_ram_name).set('vaddr', hex(RAM))

        wifi_vm = require_one(
            (vm for vm in wifi_pd.findall('virtual_machine')
             if vm.get('name') ==
             'cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM'),
            "Wi-Fi virtual machine")
        mapping(wifi_vm, guest_ram_name).set('vaddr', hex(RAM))
        mapping(wifi_vm, gic_name).set('vaddr', hex(GIC_VM))
        mapping(wifi_vm, serial_name).set('vaddr', hex(Serial))

        for irq in wifi_pd.findall('irq'):
            wifi_pd.remove(irq)
        ET.SubElement(
            wifi_pd, 'irq', irq=str(Serial_IRQ), id='1')
        ET.SubElement(
            wifi_pd, 'irq', irq=str(Internet_IRQ), id='2')
        if board.name == "rpi4b_4gb":
            ET.SubElement(wifi_pd, 'irq', irq='65', id='3')
            ET.SubElement(wifi_pd, 'irq', irq='66', id='4')

        data_storage_pd = require_one(
            (pd for pd in root.iter('protection_domain')
             if pd.get('name') ==
             'cpuSw_dataManager_dataStorage_dataStorage'),
            "data-storage VMM protection domain")
        for irq in data_storage_pd.findall('irq'):
            data_storage_pd.remove(irq)

        data_storage_region_prefix = (
            "GroundStation_Impl_Instance_cpuSw_dataManager_"
            "dataStorage_dataStorage_VM_")
        for region_suffix in ('Guest_RAM', 'GIC', 'Serial'):
            memory_region(
                data_storage_region_prefix + region_suffix
            ).attrib.pop('phys_addr', None)

        ET.indent(root, space='  ')
        return ET.tostring(
            root, encoding='unicode', xml_declaration=True)

    with open(f"{output_dir}/{sdf_path}", "w+") as f:
        f.write(apply_platform_overrides(sdf.render()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dtb", required=True)
    parser.add_argument("--sddf", required=True)
    parser.add_argument("--board", required=True, choices=[b.name for b in BOARDS])
    parser.add_argument("--output", required=True)
    parser.add_argument("--sdf", required=True)
    parser.add_argument("--objcopy", required=True)

    args = parser.parse_args()

    # Import the config structs module from the build directory
    sys.path.append(args.output)
    from config_structs import *

    board = next(filter(lambda b: b.name == args.board, BOARDS))

    sdf = SystemDescription(board.arch, board.paddr_top)
    sddf = Sddf(args.sddf)

    global obj_copy
    obj_copy = args.objcopy

    with open(args.dtb, "rb") as f:
        dtb = DeviceTree(f.read())

    generate(args.sdf, args.output, dtb)
