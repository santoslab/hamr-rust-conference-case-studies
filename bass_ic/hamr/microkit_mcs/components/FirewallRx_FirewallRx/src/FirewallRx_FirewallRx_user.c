#include "FirewallRx_FirewallRx.h"

// This file will not be overwritten if HAMR codegen is rerun

void FirewallRx_FirewallRx_initialize(void) {
  printf("%s: FirewallRx_FirewallRx_initialize invoked\n", microkit_name);
}

void FirewallRx_FirewallRx_timeTriggered(void) {
  printf("%s: FirewallRx_FirewallRx_timeTriggered invoked\n", microkit_name);
}

void FirewallRx_FirewallRx_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
