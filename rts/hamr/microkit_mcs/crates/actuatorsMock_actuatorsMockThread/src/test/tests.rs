// This file will not be overwritten if HAMR codegen is rerun

mod tests {
  // NOTE: need to run tests sequentially to prevent race conditions
  //       on the app and the testing apis which are static
  use serial_test::serial;

  use crate::test::util::*;
  use data::*;

  #[test]
  #[serial]
  fn test_initialization() {
    crate::actuatorsMock_actuatorsMockThread_initialize();
  }

  #[test]
  #[serial]
  fn test_compute() {
    crate::actuatorsMock_actuatorsMockThread_initialize();

    // populate incoming data ports
    test_apis::put_tempPressureActuate(false);
    test_apis::put_saturationActuate(false);

    crate::actuatorsMock_actuatorsMockThread_timeTriggered();
  }
}
