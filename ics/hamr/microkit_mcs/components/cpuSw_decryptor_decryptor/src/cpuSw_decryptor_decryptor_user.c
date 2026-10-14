#include "cpuSw_decryptor_decryptor.h"

// This file will not be overwritten if HAMR codegen is rerun

void cpuSw_decryptor_decryptor_initialize(void) {
  printf("%s: cpuSw_decryptor_decryptor_initialize invoked\n", microkit_name);
}

void cpuSw_decryptor_decryptor_timeTriggered(void) {
  printf("%s: cpuSw_decryptor_decryptor_timeTriggered invoked\n", microkit_name);
}

void cpuSw_decryptor_decryptor_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
