#include "eventControlMock_eventControlMockThread.h"

// This file will not be overwritten if HAMR codegen is rerun

void eventControlMock_eventControlMockThread_initialize(void) {
  printf("%s: eventControlMock_eventControlMockThread_initialize invoked\n", microkit_name);
}

void eventControlMock_eventControlMockThread_timeTriggered(void) {
  printf("%s: eventControlMock_eventControlMockThread_timeTriggered invoked\n", microkit_name);
}

void eventControlMock_eventControlMockThread_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
