#include "FirewallTx_FirewallTx.h"

// This file will not be overwritten if HAMR codegen is rerun

void FirewallTx_FirewallTx_initialize(void) {
  printf("%s: FirewallTx_FirewallTx_initialize invoked\n", microkit_name);
}

void FirewallTx_FirewallTx_timeTriggered(void) {
  printf("%s: FirewallTx_FirewallTx_timeTriggered invoked\n", microkit_name);
}

void FirewallTx_FirewallTx_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
