#include "cpuSw_encryptor_encryptor.h"

// This file will not be overwritten if HAMR codegen is rerun

void cpuSw_encryptor_encryptor_initialize(void) {
  printf("%s: cpuSw_encryptor_encryptor_initialize invoked\n", microkit_name);
}

void cpuSw_encryptor_encryptor_timeTriggered(void) {
  printf("%s: cpuSw_encryptor_encryptor_timeTriggered invoked\n", microkit_name);
}

void cpuSw_encryptor_encryptor_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
