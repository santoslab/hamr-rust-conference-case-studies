#include "cpuSw_dataAnalysis_dataAnalysis.h"

// This file will not be overwritten if HAMR codegen is rerun

void cpuSw_dataAnalysis_dataAnalysis_initialize(void) {
  printf("%s: cpuSw_dataAnalysis_dataAnalysis_initialize invoked\n", microkit_name);
}

void cpuSw_dataAnalysis_dataAnalysis_timeTriggered(void) {
  printf("%s: cpuSw_dataAnalysis_dataAnalysis_timeTriggered invoked\n", microkit_name);
}

void cpuSw_dataAnalysis_dataAnalysis_notify(microkit_channel channel) {
  // this method is called when the monitor does not handle the passed in channel
  switch (channel) {
    default:
      printf("%s: Unexpected channel %d\n", microkit_name, channel);
  }
}
