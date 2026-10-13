#include "actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator.h"

// This file will not be overwritten if HAMR codegen is rerun

void actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_initialize(void) {
  printf("%s: actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_initialize invoked\n", microkit_name);
}

void actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_timeTriggered(void) {
  printf("%s: actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_timeTriggered invoked\n", microkit_name);
}

void actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
