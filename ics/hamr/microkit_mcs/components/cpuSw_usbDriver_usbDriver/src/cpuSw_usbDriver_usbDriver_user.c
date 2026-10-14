#include "cpuSw_usbDriver_usbDriver.h"

// This file will not be overwritten if HAMR codegen is rerun

void cpuSw_usbDriver_usbDriver_initialize(void) {
  printf("%s: cpuSw_usbDriver_usbDriver_initialize invoked\n", microkit_name);
}

void cpuSw_usbDriver_usbDriver_timeTriggered(void) {
  printf("%s: cpuSw_usbDriver_usbDriver_timeTriggered invoked\n", microkit_name);
}

void cpuSw_usbDriver_usbDriver_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
