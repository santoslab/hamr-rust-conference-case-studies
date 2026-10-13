#include "actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic.h"

// This file will not be overwritten if HAMR codegen is rerun

void actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_initialize(void) {
  printf("%s: actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_initialize invoked\n", microkit_name);
}

void actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_timeTriggered(void) {
  printf("%s: actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_timeTriggered invoked\n", microkit_name);
}

void actuationSubsystem_actuationUnit1_tempPressureTripOut_orLogic_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
