#include "actuatorsMock_actuatorsMockThread.h"

// This file will not be overwritten if HAMR codegen is rerun

void actuatorsMock_actuatorsMockThread_initialize(void) {
  printf("%s: actuatorsMock_actuatorsMockThread_initialize invoked\n", microkit_name);
}

void actuatorsMock_actuatorsMockThread_timeTriggered(void) {
  printf("%s: actuatorsMock_actuatorsMockThread_timeTriggered invoked\n", microkit_name);
}

void actuatorsMock_actuatorsMockThread_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
