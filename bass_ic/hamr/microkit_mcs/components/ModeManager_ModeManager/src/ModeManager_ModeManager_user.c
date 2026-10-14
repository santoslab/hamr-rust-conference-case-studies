#include "ModeManager_ModeManager.h"

// This file will not be overwritten if HAMR codegen is rerun

void ModeManager_ModeManager_initialize(void) {
  printf("%s: ModeManager_ModeManager_initialize invoked\n", microkit_name);
}

void ModeManager_ModeManager_timeTriggered(void) {
  printf("%s: ModeManager_ModeManager_timeTriggered invoked\n", microkit_name);
}

void ModeManager_ModeManager_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
