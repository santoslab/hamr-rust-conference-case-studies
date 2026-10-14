#include "cpuSw_wifiDriver_wifiDriver_wifiDriver.h"

// This file will not be overwritten if HAMR codegen is rerun

void cpuSw_wifiDriver_wifiDriver_wifiDriver_initialize(void) {
  printf("%s: cpuSw_wifiDriver_wifiDriver_wifiDriver_initialize invoked\n", microkit_name);
}

void cpuSw_wifiDriver_wifiDriver_wifiDriver_timeTriggered(void) {
  printf("%s: cpuSw_wifiDriver_wifiDriver_wifiDriver_timeTriggered invoked\n", microkit_name);
}

void cpuSw_wifiDriver_wifiDriver_wifiDriver_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
