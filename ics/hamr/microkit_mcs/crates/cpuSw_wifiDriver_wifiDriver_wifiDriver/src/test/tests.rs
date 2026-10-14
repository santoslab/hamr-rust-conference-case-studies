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
    crate::cpuSw_wifiDriver_wifiDriver_wifiDriver_initialize();
  }

  #[test]
  #[serial]
  fn test_compute() {
    crate::cpuSw_wifiDriver_wifiDriver_wifiDriver_initialize();
    crate::cpuSw_wifiDriver_wifiDriver_wifiDriver_timeTriggered();
  }
}

mod GUMBOX_tests {
  use serial_test::serial;
  use proptest::prelude::*;

  use crate::test::util::*;
  use crate::testInitializeCB_macro;
  use crate::testComputeCB_macro;
    use crate::testComputeCBwGSV_macro;

  // number of valid (i.e., non-rejected) test cases that must be executed for the compute method.
  const numValidComputeTestCases: u32 = 100;

  // how many total test cases (valid + rejected) that may be attempted.
  //   0 means all inputs must satisfy the precondition (if present),
  //   5 means at most 5 rejected inputs are allowed per valid test case
  const computeRejectRatio: u32 = 5;

  const verbosity: u32 = 2;

  testInitializeCB_macro! {
    prop_testInitializeCB_macro, // test name
    config: ProptestConfig { // proptest configuration, built by overriding fields from default config
      cases: numValidComputeTestCases,
      max_global_rejects: numValidComputeTestCases * computeRejectRatio,
      verbose: verbosity,
      ..ProptestConfig::default()
    }
  }

  testComputeCB_macro! {
    prop_testComputeCB_macro, // test name
    config: ProptestConfig { // proptest configuration, built by overriding fields from default config
      cases: numValidComputeTestCases,
      max_global_rejects: numValidComputeTestCases * computeRejectRatio,
      verbose: verbosity,
      ..ProptestConfig::default()
    },
    // strategies for generating each component input
    // TODO: full-range default; if alert_in is constrained by a GUMBO assume clause then
    //       narrow this strategy (e.g. generators::u8_strategy_cust(lou8..=hiu8))
    //       to avoid exhausting the proptest rejection budget
    api_alert_in: generators::option_strategy_default(generators::u8_strategy_default()),
    api_analysis_report: generators::option_strategy_default(generators::Common_OutgoingWifiMessage_Impl_strategy_default()),
    api_wifiRecv: generators::option_strategy_default(generators::Common_IncomingWifiMessage_Impl_strategy_default())
  }

  testComputeCBwGSV_macro! {
    prop_testComputeCBwGSV_macro, // test name
    config: ProptestConfig { // proptest configuration, built by overriding fields from default config
      cases: numValidComputeTestCases,
      max_global_rejects: numValidComputeTestCases * computeRejectRatio,
      verbose: verbosity,
      ..ProptestConfig::default()
    },
    // strategies for generating each component input
    In_alert_cmd: generators::bool_strategy_default(),
    // TODO: full-range default; if alert_in is constrained by a GUMBO assume clause then
    //       narrow this strategy (e.g. generators::u8_strategy_cust(lou8..=hiu8))
    //       to avoid exhausting the proptest rejection budget
    api_alert_in: generators::option_strategy_default(generators::u8_strategy_default()),
    api_analysis_report: generators::option_strategy_default(generators::Common_OutgoingWifiMessage_Impl_strategy_default()),
    api_wifiRecv: generators::option_strategy_default(generators::Common_IncomingWifiMessage_Impl_strategy_default())
  }
}
