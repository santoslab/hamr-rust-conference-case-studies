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
    instrumentationMock_instrumentationMockThread_MON = ProtectionDomain(
      name="instrumentationMock_instrumentationMockThread_MON",
      program_image="instrumentationMock_instrumentationMockThread_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(instrumentationMock_instrumentationMockThread_MON)

    instrumentationMock_instrumentationMockThread = ProtectionDomain(
      name="instrumentationMock_instrumentationMockThread",
      program_image="instrumentationMock_instrumentationMockThread.elf",
      priority=140,
      passive=True)
    instrumentationMock_instrumentationMockThread_MON.add_child_pd(instrumentationMock_instrumentationMockThread, child_id=1)

    eventControlMock_eventControlMockThread_MON = ProtectionDomain(
      name="eventControlMock_eventControlMockThread_MON",
      program_image="eventControlMock_eventControlMockThread_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(eventControlMock_eventControlMockThread_MON)

    eventControlMock_eventControlMockThread = ProtectionDomain(
      name="eventControlMock_eventControlMockThread",
      program_image="eventControlMock_eventControlMockThread.elf",
      priority=140,
      passive=True)
    eventControlMock_eventControlMockThread_MON.add_child_pd(eventControlMock_eventControlMockThread, child_id=1)

    actuatorsMock_actuatorsMockThread_MON = ProtectionDomain(
      name="actuatorsMock_actuatorsMockThread_MON",
      program_image="actuatorsMock_actuatorsMockThread_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuatorsMock_actuatorsMockThread_MON)

    actuatorsMock_actuatorsMockThread = ProtectionDomain(
      name="actuatorsMock_actuatorsMockThread",
      program_image="actuatorsMock_actuatorsMockThread.elf",
      priority=140,
      passive=True)
    actuatorsMock_actuatorsMockThread_MON.add_child_pd(actuatorsMock_actuatorsMockThread, child_id=1)

    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON",
      program_image="actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON)

    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic",
      program_image="actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON.add_child_pd(actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic, child_id=1)

    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON",
      program_image="actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON)

    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic",
      program_image="actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON.add_child_pd(actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic, child_id=1)

    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON",
      program_image="actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON)

    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic",
      program_image="actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON.add_child_pd(actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic, child_id=1)

    actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON",
      program_image="actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON)

    actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic",
      program_image="actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON.add_child_pd(actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic, child_id=1)

    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON",
      program_image="actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON)

    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic",
      program_image="actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON.add_child_pd(actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic, child_id=1)

    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON",
      program_image="actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON)

    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic",
      program_image="actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON.add_child_pd(actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic, child_id=1)

    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON",
      program_image="actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON)

    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic",
      program_image="actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON.add_child_pd(actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic, child_id=1)

    actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON",
      program_image="actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON)

    actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic = ProtectionDomain(
      name="actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic",
      program_image="actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON.add_child_pd(actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic, child_id=1)

    actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON = ProtectionDomain(
      name="actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON",
      program_image="actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON)

    actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic = ProtectionDomain(
      name="actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic",
      program_image="actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON.add_child_pd(actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic, child_id=1)

    actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON = ProtectionDomain(
      name="actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON",
      program_image="actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON)

    actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator = ProtectionDomain(
      name="actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator",
      program_image="actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator.elf",
      priority=140,
      passive=True)
    actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON.add_child_pd(actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator, child_id=1)

    actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON = ProtectionDomain(
      name="actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON",
      program_image="actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON)

    actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic = ProtectionDomain(
      name="actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic",
      program_image="actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic.elf",
      priority=140,
      passive=True)
    actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON.add_child_pd(actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic, child_id=1)

    actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON = ProtectionDomain(
      name="actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON",
      program_image="actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON.elf",
      priority=150,
      passive=True)
    scheduler.add_child_pd(actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON)

    actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator = ProtectionDomain(
      name="actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator",
      program_image="actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator.elf",
      priority=140,
      passive=True)
    actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON.add_child_pd(actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator, child_id=1)


    #######################################
    # MEMORY REGIONS
    #######################################
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel1_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel1_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel1_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel2_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel2_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel2_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel3_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel3_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel3_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel4_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel4_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel4_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel1_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel1_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel1_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel2_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel2_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel2_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel3_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel3_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel3_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel4_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel4_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel4_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel1_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel1_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel1_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel2_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel2_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel2_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel3_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel3_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel3_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel4_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel4_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel4_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel1_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel1_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel1_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel2_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel2_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel2_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel3_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel3_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel3_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel4_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel4_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel4_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel1_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel1_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel1_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel2_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel2_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel2_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel3_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel3_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel3_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel4_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel4_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel4_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel1_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel1_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel1_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel2_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel2_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel2_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel3_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel3_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel3_1_Memory_Region)
    RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel4_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel4_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel4_1_Memory_Region)
    RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput1_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput1_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput1_1_Memory_Region)
    RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput2_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput2_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput2_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_output_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_output_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_output_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_actuate_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_actuate_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_actuate_1_Memory_Region)
    RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_output_1_Memory_Region = MemoryRegion(sdf, "RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_output_1_Memory_Region", 0x1_000)
    sdf.add_mr(RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_output_1_Memory_Region)

    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel1_1_Memory_Region, 0x10_000_000, perms="rw", setvar_vaddr="unit1_temperatureLogic_channel1_queue_1"))
    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel1_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel2_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="unit1_temperatureLogic_channel2_queue_1"))
    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel2_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel3_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="unit1_temperatureLogic_channel3_queue_1"))
    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel3_1_Memory_Region, 0x10_004_000, perms="r", setvar_vaddr="channel3_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel4_1_Memory_Region, 0x10_006_000, perms="rw", setvar_vaddr="unit1_temperatureLogic_channel4_queue_1"))
    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_temperatureLogic_channel4_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="channel4_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel1_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="unit1_pressureLogic_channel1_queue_1"))
    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel1_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel2_1_Memory_Region, 0x10_00A_000, perms="rw", setvar_vaddr="unit1_pressureLogic_channel2_queue_1"))
    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel2_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel3_1_Memory_Region, 0x10_00C_000, perms="rw", setvar_vaddr="unit1_pressureLogic_channel3_queue_1"))
    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel3_1_Memory_Region, 0x10_004_000, perms="r", setvar_vaddr="channel3_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel4_1_Memory_Region, 0x10_00E_000, perms="rw", setvar_vaddr="unit1_pressureLogic_channel4_queue_1"))
    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_pressureLogic_channel4_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="channel4_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel1_1_Memory_Region, 0x10_010_000, perms="rw", setvar_vaddr="unit1_saturationLogic_channel1_queue_1"))
    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel1_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel2_1_Memory_Region, 0x10_012_000, perms="rw", setvar_vaddr="unit1_saturationLogic_channel2_queue_1"))
    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel2_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel3_1_Memory_Region, 0x10_014_000, perms="rw", setvar_vaddr="unit1_saturationLogic_channel3_queue_1"))
    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel3_1_Memory_Region, 0x10_004_000, perms="r", setvar_vaddr="channel3_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel4_1_Memory_Region, 0x10_016_000, perms="rw", setvar_vaddr="unit1_saturationLogic_channel4_queue_1"))
    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit1_saturationLogic_channel4_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="channel4_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel1_1_Memory_Region, 0x10_018_000, perms="rw", setvar_vaddr="unit2_temperatureLogic_channel1_queue_1"))
    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel1_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel2_1_Memory_Region, 0x10_01A_000, perms="rw", setvar_vaddr="unit2_temperatureLogic_channel2_queue_1"))
    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel2_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel3_1_Memory_Region, 0x10_01C_000, perms="rw", setvar_vaddr="unit2_temperatureLogic_channel3_queue_1"))
    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel3_1_Memory_Region, 0x10_004_000, perms="r", setvar_vaddr="channel3_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel4_1_Memory_Region, 0x10_01E_000, perms="rw", setvar_vaddr="unit2_temperatureLogic_channel4_queue_1"))
    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_temperatureLogic_channel4_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="channel4_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel1_1_Memory_Region, 0x10_020_000, perms="rw", setvar_vaddr="unit2_pressureLogic_channel1_queue_1"))
    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel1_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel2_1_Memory_Region, 0x10_022_000, perms="rw", setvar_vaddr="unit2_pressureLogic_channel2_queue_1"))
    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel2_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel3_1_Memory_Region, 0x10_024_000, perms="rw", setvar_vaddr="unit2_pressureLogic_channel3_queue_1"))
    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel3_1_Memory_Region, 0x10_004_000, perms="r", setvar_vaddr="channel3_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel4_1_Memory_Region, 0x10_026_000, perms="rw", setvar_vaddr="unit2_pressureLogic_channel4_queue_1"))
    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_pressureLogic_channel4_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="channel4_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel1_1_Memory_Region, 0x10_028_000, perms="rw", setvar_vaddr="unit2_saturationLogic_channel1_queue_1"))
    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel1_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel2_1_Memory_Region, 0x10_02A_000, perms="rw", setvar_vaddr="unit2_saturationLogic_channel2_queue_1"))
    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel2_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel3_1_Memory_Region, 0x10_02C_000, perms="rw", setvar_vaddr="unit2_saturationLogic_channel3_queue_1"))
    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel3_1_Memory_Region, 0x10_004_000, perms="r", setvar_vaddr="channel3_queue_1"))
    instrumentationMock_instrumentationMockThread.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel4_1_Memory_Region, 0x10_02E_000, perms="rw", setvar_vaddr="unit2_saturationLogic_channel4_queue_1"))
    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_instrumentationMock_instrumentationMockThread_unit2_saturationLogic_channel4_1_Memory_Region, 0x10_006_000, perms="r", setvar_vaddr="channel4_queue_1"))
    eventControlMock_eventControlMockThread.add_map(Map(RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput1_1_Memory_Region, 0x10_000_000, perms="rw", setvar_vaddr="manualActuatorInput1_queue_1"))
    actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator.add_map(Map(RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput1_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="manualActuatorInput_queue_1"))
    eventControlMock_eventControlMockThread.add_map(Map(RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput2_1_Memory_Region, 0x10_002_000, perms="rw", setvar_vaddr="manualActuatorInput2_queue_1"))
    actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator.add_map(Map(RTS_i_Instance_eventControlMock_eventControlMockThread_manualActuatorInput2_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="manualActuatorInput_queue_1"))
    actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_actuate_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_actuate_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="channel1_queue_1"))
    actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_008_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_actuate_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_actuate_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_actuate_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="channel2_queue_1"))
    actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_actuate_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator.add_map(Map(RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_actuate_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="input_queue_1"))
    actuatorsMock_actuatorsMockThread.add_map(Map(RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_output_1_Memory_Region, 0x10_000_000, perms="r", setvar_vaddr="tempPressureActuate_queue_1"))
    actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator.add_map(Map(RTS_i_Instance_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_output_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="output_queue_1"))
    actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic.add_map(Map(RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_actuate_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="actuate_queue_1"))
    actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator.add_map(Map(RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_actuate_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="input_queue_1"))
    actuatorsMock_actuatorsMockThread.add_map(Map(RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_output_1_Memory_Region, 0x10_002_000, perms="r", setvar_vaddr="saturationActuate_queue_1"))
    actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator.add_map(Map(RTS_i_Instance_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_output_1_Memory_Region, 0x10_004_000, perms="rw", setvar_vaddr="output_queue_1"))



    #######################################
    # CHANNELS
    #######################################
    channel_instrumentationMock_instrumentationMockThread_MON = 2
    channel_eventControlMock_eventControlMockThread_MON = 3
    channel_actuatorsMock_actuatorsMockThread_MON = 4
    channel_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON = 5
    channel_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON = 6
    channel_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON = 7
    channel_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON = 8
    channel_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON = 9
    channel_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON = 10
    channel_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON = 11
    channel_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON = 12
    channel_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON = 13
    channel_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON = 14
    channel_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON = 15
    channel_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON = 16

    sdf.add_channel(Channel(a=scheduler, a_id=2, b=instrumentationMock_instrumentationMockThread_MON, b_id=0))
    sdf.add_channel(Channel(a=instrumentationMock_instrumentationMockThread_MON, a_id=1, b=instrumentationMock_instrumentationMockThread, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=3, b=eventControlMock_eventControlMockThread_MON, b_id=0))
    sdf.add_channel(Channel(a=eventControlMock_eventControlMockThread_MON, a_id=1, b=eventControlMock_eventControlMockThread, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=4, b=actuatorsMock_actuatorsMockThread_MON, b_id=0))
    sdf.add_channel(Channel(a=actuatorsMock_actuatorsMockThread_MON, a_id=1, b=actuatorsMock_actuatorsMockThread, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=5, b=actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=6, b=actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=7, b=actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=8, b=actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=9, b=actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=10, b=actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=11, b=actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=12, b=actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON, a_id=1, b=actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=13, b=actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON, a_id=1, b=actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=14, b=actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON, a_id=1, b=actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=15, b=actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON, a_id=1, b=actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic, b_id=0))
    sdf.add_channel(Channel(a=scheduler, a_id=16, b=actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON, b_id=0))
    sdf.add_channel(Channel(a=actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON, a_id=1, b=actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator, b_id=0))

    #######################################
    # SCHEDULE
    #######################################
    ts_instrumentationMock_instrumentationMockThread_MON = (channel_instrumentationMock_instrumentationMockThread_MON, 10000000, True)
    ts_eventControlMock_eventControlMockThread_MON = (channel_eventControlMock_eventControlMockThread_MON, 10000000, True)
    ts_actuatorsMock_actuatorsMockThread_MON = (channel_actuatorsMock_actuatorsMockThread_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON = (channel_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON = (channel_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON = (channel_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON = (channel_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON = (channel_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON = (channel_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON = (channel_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON, 10000000, True)
    ts_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON = (channel_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON, 10000000, True)
    ts_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON = (channel_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON, 10000000, True)
    ts_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON = (channel_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON, 10000000, True)
    ts_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON = (channel_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON, 10000000, True)
    ts_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON = (channel_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON, 10000000, True)
    ts_pad = (0, 850000000, False)

    user_schedule = schedule(
      ts_instrumentationMock_instrumentationMockThread_MON,
      ts_eventControlMock_eventControlMockThread_MON,
      ts_actuatorsMock_actuatorsMockThread_MON,
      ts_actuationSubsystem_actuationUnit1_temperatureLogic_coincidenceLogic_MON,
      ts_actuationSubsystem_actuationUnit1_pressureLogic_coincidenceLogic_MON,
      ts_actuationSubsystem_actuationUnit1_saturationLogic_coincidenceLogic_MON,
      ts_actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_MON,
      ts_actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_MON,
      ts_actuationSubsystem_actuationUnit2_pressureLogic_coincidenceLogic_MON,
      ts_actuationSubsystem_actuationUnit2_saturationLogic_coincidenceLogic_MON,
      ts_actuationSubsystem_actuationUnit2_tempPressureTripOut_orLogic_MON,
      ts_actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_MON,
      ts_actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_MON,
      ts_actuationSubsystem_saturationActuatorUnit_actuateSaturationActuator_orLogic_MON,
      ts_actuationSubsystem_saturationActuatorUnit_saturationActuator_actuator_MON,
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
