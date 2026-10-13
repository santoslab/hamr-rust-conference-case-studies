#include "instrumentationMock_instrumentationMockThread.h"

// This file will not be overwritten if HAMR codegen is rerun

void instrumentationMock_instrumentationMockThread_initialize(void) {
  printf("%s: instrumentationMock_instrumentationMockThread_initialize invoked\n", microkit_name);
}

void instrumentationMock_instrumentationMockThread_timeTriggered(void) {
  printf("%s: instrumentationMock_instrumentationMockThread_timeTriggered invoked\n", microkit_name);
}

void instrumentationMock_instrumentationMockThread_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
