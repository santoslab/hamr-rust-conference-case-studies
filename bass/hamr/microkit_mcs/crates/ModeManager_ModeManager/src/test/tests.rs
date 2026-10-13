// This file will not be overwritten if HAMR codegen is rerun

mod tests {
  // NOTE: need to run tests sequentially to prevent race conditions
  //       on the app and the testing apis which are static
  use serial_test::serial;

  use crate::test::util::*;
  use data::*;

  // Helper: one compute dispatch with the given attack-status inputs;
  // returns the broadcast mode sampled from the CurrentMode DataPort.
  fn dispatch(rx: SW::AttackStatus, tx: SW::AttackStatus) -> SW::Mode {
    test_apis::put_AttackStatusRx(rx);
    test_apis::put_AttackStatusTx(tx);
    crate::ModeManager_ModeManager_timeTriggered();
    test_apis::get_CurrentMode()
  }

  #[test]
  #[serial]
  fn test_initialization() {
    // ModeManager_Req_Init: start in Init with zero activations; the mode
    // DataPort must read Init before any compute dispatch.
    crate::ModeManager_ModeManager_initialize();
    assert_eq!(test_apis::get_CurrentMode(), SW::Mode::Init);
    assert_eq!(test_apis::get_currentMode(), SW::Mode::Init);
    assert_eq!(test_apis::get_activationCount(), 0);
  }

  #[test]
  #[serial]
  fn test_compute() {
    crate::ModeManager_ModeManager_initialize();

    // populate incoming data ports
    test_apis::put_AttackStatusRx(SW::AttackStatus::default());
    test_apis::put_AttackStatusTx(SW::AttackStatus::default());

    crate::ModeManager_ModeManager_timeTriggered();
  }

  #[test]
  #[serial]
  fn test_CR01_init_to_normal_at_10th_activation() {
    // ModeManager_Req_StayInit / ModeManager_Req_ToNormal / ModeManager_Req_Count:
    // with no attack reported, mode is Init through dispatch 9 and becomes
    // Normal on the 10th dispatch (change-plan §9 acceptance criterion 1a).
    crate::ModeManager_ModeManager_initialize();
    for i in 1..=9 {
      let mode = dispatch(SW::AttackStatus::OK, SW::AttackStatus::OK);
      assert_eq!(mode, SW::Mode::Init, "dispatch {i}: should still be Init");
      assert_eq!(test_apis::get_activationCount(), i);
    }
    let mode = dispatch(SW::AttackStatus::OK, SW::AttackStatus::OK);
    assert_eq!(mode, SW::Mode::Normal, "10th dispatch: should be Normal");
    assert_eq!(test_apis::get_activationCount(), 10);

    // ModeManager_Req_StayNormal + counter saturation at 10
    let mode = dispatch(SW::AttackStatus::OK, SW::AttackStatus::OK);
    assert_eq!(mode, SW::Mode::Normal);
    assert_eq!(test_apis::get_activationCount(), 10, "counter saturates at 10");
  }

  #[test]
  #[serial]
  fn test_CR01_init_to_rtl_on_rx_attack() {
    // ModeManager_Req_ToRTL from Init (RTL reachable directly from Init) +
    // ModeManager_Req_Absorbing (change-plan §9 acceptance criterion 1b).
    crate::ModeManager_ModeManager_initialize();
    let mode = dispatch(SW::AttackStatus::Attack, SW::AttackStatus::OK);
    assert_eq!(mode, SW::Mode::RTL, "RX attack in Init drives RTL");

    // absorbing: attack cleared, mode must remain RTL past the 10th activation
    for _ in 0..12 {
      let mode = dispatch(SW::AttackStatus::OK, SW::AttackStatus::OK);
      assert_eq!(mode, SW::Mode::RTL, "RTL is absorbing until restart");
    }
  }

  #[test]
  #[serial]
  fn test_CR01_normal_to_rtl_on_tx_attack() {
    // ModeManager_Req_ToRTL from Normal (change-plan §9 acceptance criterion 1c).
    crate::ModeManager_ModeManager_initialize();
    for _ in 1..=10 {
      dispatch(SW::AttackStatus::OK, SW::AttackStatus::OK);
    }
    assert_eq!(test_apis::get_CurrentMode(), SW::Mode::Normal);

    let mode = dispatch(SW::AttackStatus::OK, SW::AttackStatus::Attack);
    assert_eq!(mode, SW::Mode::RTL, "TX attack in Normal drives RTL");

    let mode = dispatch(SW::AttackStatus::OK, SW::AttackStatus::OK);
    assert_eq!(mode, SW::Mode::RTL, "RTL is absorbing");
  }

  #[test]
  #[serial]
  fn test_notify_unknown_channel() {
    // coverage: the notify entry point logs and ignores unknown channels
    crate::ModeManager_ModeManager_initialize();
    crate::ModeManager_ModeManager_notify(9999);
  }

  #[test]
  #[serial]
  fn test_CR01_attack_wins_tie_on_10th_activation() {
    // ModeManager_Req_ToRTL wins ties: on the dispatch where the counter
    // reaches 10, a simultaneous attack report yields RTL, not Normal.
    crate::ModeManager_ModeManager_initialize();
    test_apis::put_currentMode(SW::Mode::Init);
    test_apis::put_activationCount(9);
    let mode = dispatch(SW::AttackStatus::Attack, SW::AttackStatus::Attack);
    assert_eq!(mode, SW::Mode::RTL, "attack wins the tie against Init-to-Normal");
  }
}

mod GUMBOX_manual_tests {
  use serial_test::serial;

  use crate::test::util::*;
  use data::*;

  #[test]
  #[serial]
  fn test_GUMBOX_manual_no_attack() {
    // From a freshly initialized state (Init, count 0), an OK/OK dispatch
    // must satisfy the full compute contract.
    let result = cb_apis::testComputeCB(SW::AttackStatus::OK, SW::AttackStatus::OK);
    assert!(matches!(result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_GUMBOX_manual_attack_from_init() {
    let result = cb_apis::testComputeCB(SW::AttackStatus::Attack, SW::AttackStatus::OK);
    assert!(matches!(result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_GUMBOX_manual_wGSV_tie_on_10th() {
    // Pre-state (Init, 9) with an attack: contract requires RTL.
    let result = cb_apis::testComputeCBwGSV(
      9, SW::Mode::Init, SW::AttackStatus::Attack, SW::AttackStatus::OK);
    assert!(matches!(result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_GUMBOX_manual_wGSV_normal_boundary() {
    // Pre-state (Init, 9) with no attack: contract requires Normal.
    let result = cb_apis::testComputeCBwGSV(
      9, SW::Mode::Init, SW::AttackStatus::OK, SW::AttackStatus::OK);
    assert!(matches!(result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_GUMBOX_manual_wGSV_rtl_absorbing() {
    // Pre-state RTL with no attack: contract requires RTL.
    let result = cb_apis::testComputeCBwGSV(
      10, SW::Mode::RTL, SW::AttackStatus::OK, SW::AttackStatus::OK);
    assert!(matches!(result, cb_apis::HarnessResult::Passed));
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
    api_AttackStatusRx: generators::SW_AttackStatus_strategy_default(),
    api_AttackStatusTx: generators::SW_AttackStatus_strategy_default()
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
    In_activationCount: generators::i32_strategy_default(),
    In_currentMode: generators::SW_Mode_strategy_default(),
    api_AttackStatusRx: generators::SW_AttackStatus_strategy_default(),
    api_AttackStatusTx: generators::SW_AttackStatus_strategy_default()
  }
}

//============================================================================
//  Specification Audit Tests (/audit-gumbo-contracts, full mode, CR-01)
//
//  These tests probe the SPECIFICATION directly by evaluating the generated
//  GUMBOX oracle functions on constructed pre/post-state pairs — they never
//  invoke the implementation (no test_apis / cb_apis). The audit scored zero
//  findings (reports/CR01-specification-audit-ModeManager.md), so these are
//  ADEQUACY PROBES backing that verdict:
//    audit_A*  — the oracle ACCEPTS an intended behavior (assert  Post(...));
//    audit_R*  — the oracle REJECTS a wrong behavior     (assert !Post(...)).
//  Every test passing = the zero-findings verdict is confirmed against the
//  woven oracle, not just the model text. Argument order for compute_CEP_Post:
//  (In_activationCount, In_currentMode, activationCount, currentMode,
//   api_AttackStatusRx, api_AttackStatusTx, api_CurrentMode).
//============================================================================
mod specification_audit_tests {
  use serial_test::serial;
  use crate::bridge::ModeManager_ModeManager_GUMBOX as GUMBOX;
  use data::*;

  const OK: SW::AttackStatus = SW::AttackStatus::OK;
  const ATTACK: SW::AttackStatus = SW::AttackStatus::Attack;
  const INIT: SW::Mode = SW::Mode::Init;
  const NORMAL: SW::Mode = SW::Mode::Normal;
  const RTL: SW::Mode = SW::Mode::RTL;

  // ---- acceptance probes: intended behaviors satisfy the oracle ----

  #[test]
  #[serial]
  fn audit_A1_nominal_init_step_accepted() {
    // Partition row "Init, no attack, post-count < 10" (StayInit)
    assert!(GUMBOX::compute_CEP_Post(0, INIT, 1, INIT, OK, OK, INIT),
      "nominal Init step must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A2_normal_boundary_at_10th_accepted() {
    // Partition row "Init, no attack, post-count >= 10" (ToNormal)
    assert!(GUMBOX::compute_CEP_Post(9, INIT, 10, NORMAL, OK, OK, NORMAL),
      "10th activation transitioning to Normal must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A3_rtl_from_init_on_attack_accepted() {
    // Partition row "non-RTL, attack reported" (ToRTL) — from Init
    assert!(GUMBOX::compute_CEP_Post(3, INIT, 4, RTL, ATTACK, OK, RTL),
      "attack during Init driving RTL must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A4_rtl_absorbing_accepted() {
    // Partition row "In(currentMode) == RTL" (Absorbing)
    assert!(GUMBOX::compute_CEP_Post(10, RTL, 10, RTL, OK, OK, RTL),
      "staying in RTL must satisfy the contract");
  }

  // ---- rejection probes: wrong behaviors violate the oracle ----

  #[test]
  #[serial]
  fn audit_R1_tie_going_normal_rejected() {
    // CR01_MM_ToRTL wins ties: count reaches 10 AND attack -> Normal is wrong
    assert!(!GUMBOX::compute_CEP_Post(9, INIT, 10, NORMAL, ATTACK, OK, NORMAL),
      "CR01_MM_ToRTL must reject Normal on a 10th-activation/attack tie");
  }

  #[test]
  #[serial]
  fn audit_R2_premature_normal_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(3, INIT, 4, NORMAL, OK, OK, NORMAL),
      "CR01_MM_StayInit must reject Normal before the 10th activation");
  }

  #[test]
  #[serial]
  fn audit_R3_rtl_exit_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(10, RTL, 10, NORMAL, OK, OK, NORMAL),
      "CR01_MM_Absorbing must reject any exit from RTL");
  }

  #[test]
  #[serial]
  fn audit_R4_missing_increment_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(5, INIT, 5, INIT, OK, OK, INIT),
      "CR01_MM_Count must reject a non-incremented counter below 10");
  }

  #[test]
  #[serial]
  fn audit_R5_counter_past_saturation_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(10, NORMAL, 11, NORMAL, OK, OK, NORMAL),
      "CR01_MM_Count must reject counting past the saturation bound 10");
  }

  #[test]
  #[serial]
  fn audit_R6_broadcast_mismatch_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(0, INIT, 1, INIT, OK, OK, NORMAL),
      "CR01_MM_Broadcast must reject an output port differing from the mode state");
  }

  #[test]
  #[serial]
  fn audit_R7_normal_ignoring_attack_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(10, NORMAL, 10, NORMAL, OK, ATTACK, NORMAL),
      "CR01_MM_ToRTL must reject staying in Normal when TX reports Attack");
  }

  // ---- initialize probes ----

  #[test]
  #[serial]
  fn audit_A5_initialize_accepted() {
    assert!(GUMBOX::initialize_IEP_Post(0, INIT, INIT),
      "(Init, 0, port Init) must satisfy CR01_MM_Init");
  }

  #[test]
  #[serial]
  fn audit_R8_initialize_wrong_mode_rejected() {
    assert!(!GUMBOX::initialize_IEP_Post(0, NORMAL, NORMAL),
      "CR01_MM_Init must reject initialization in Normal mode");
  }

  #[test]
  #[serial]
  fn audit_R9_initialize_port_mismatch_rejected() {
    assert!(!GUMBOX::initialize_IEP_Post(0, INIT, NORMAL),
      "CR01_MM_Init must reject a mode DataPort not initialized to Init");
  }
}
