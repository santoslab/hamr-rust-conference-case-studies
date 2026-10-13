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
    crate::eventControlMock_eventControlMockThread_initialize();
  }

  #[test]
  #[serial]
  fn test_compute() {
    crate::eventControlMock_eventControlMockThread_initialize();
    crate::eventControlMock_eventControlMockThread_timeTriggered();
  }
}
