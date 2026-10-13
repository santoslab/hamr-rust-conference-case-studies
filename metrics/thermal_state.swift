// Prints macOS's thermal state (ProcessInfo.thermalState): 0 nominal, 1 fair, 2 serious,
// 3 critical. Used by verus_timing.py; compile once with: swiftc -O -o thermal_state thermal_state.swift
import Foundation
print(ProcessInfo.processInfo.thermalState.rawValue)
