// This file will not be overwritten if codegen is rerun

mod tests {
  // NOTE: need to run tests sequentially to prevent race conditions
  //       on the app and the testing apis which are static
  use serial_test::serial;

  use crate::test::util::*;
  use data::*;

  #[test]
  #[serial]
  fn test_initialization() {
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode
}

  #[test]
  #[serial]
  fn test_compute() {
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode
    crate::FirewallTx_FirewallTx_timeTriggered();
  }

  //========================================================================
  //  (RC_INSPECTA_00-HLR-7) 
  //  If the firewall gets a wellformed Arp frame from TxIn, the firewall 
  //  shall copy the frame to TxOut.
  //========================================================================

     /*
       Inputs:
         EthernetFramesTxIn = Some(m) such that:
          m.malformedFrame == false
          m.frameProtocol == ARP
          ..other fields are irrelevant..

       Expected Outputs:
         EthernetFramesTxOut = Some(m1) such that:
          m == m1
    */
  #[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_7() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode

    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {frameProtocol: SW::FrameProtocol::ARP, 
      malformedFrame: false, ..Default::default()};
 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(Some(m));

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    let reply = test_apis::get_EthernetFramesTxOut();

    // get result values from output ports
    match reply {
      Some(m1) => {
        assert_eq!(m1, m);
      }
      None => assert!(false)
    };

  }

  //========================================================================
  //  (RC_INSPECTA_00-HLR-12) 
  // If the firewall gets a wellformed IPv4 frame from TxIn, 
  // the firewall shall copy the frame to TxOut.
  //========================================================================

     /*
       Inputs:
         EthernetFramesTxIn = Some(m) such that:
          m.malformedFrame == false
          m.internetProtocol == IPv4
          ..other fields are irrelevant..

       Expected Outputs:
         EthernetFramesTxOut = Some(m1) such that:
          m == m1
    */
  #[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_12_IPv4() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode

    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {internetProtocol: SW::InternetProtocol::IPV4, 
       malformedFrame: false, ..Default::default() };

 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(Some(m));

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    // get result values from output ports
    let reply = test_apis::get_EthernetFramesTxOut();

    match reply {
      Some(m1) => {
        assert_eq!(m, m1);
      }
      None => {
        assert!(false);
      }
    }
  }

  //========================================================================
  //  (RC_INSPECTA_00-HLR-12) 
  // If the firewall gets a wellformed IPv4 frame from TxIn, 
  // the firewall shall copy the frame to TxOut.
  //========================================================================

     /*
       Inputs:
         EthernetFramesTxIn = Some(m) such that:
          m.malformedFrame == false
          m.internetProtocol == IPv4
          m.rawMessage = [50 (or any u8 that in the Naturals), SW_RawEthernetMessage_DIM_0]
          ..other fields are irrelevant..

       Expected Outputs:
         EthernetFramesTxOut = Some(m1) such that:
          m == m1
    */
  #[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_12_IPv4_Non_Default_Payload() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode

    let payload: u8 = 50;

    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {internetProtocol: SW::InternetProtocol::IPV4, 
       rawMessage: [payload; SW::SW_RawEthernetMessage_DIM_0], ..Default::default() };

 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(Some(m));

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    // get result values from output ports
    let reply = test_apis::get_EthernetFramesTxOut();

    match reply {
      Some(m1) => {
        assert_eq!(m, m1);
      }
      None => {
        assert!(false);
      }
    }

    
  }

  //========================================================================
  //  (RC_INSPECTA_00-HLR-14) 
  // If the firewall gets a malformed frame, it should drop the frame.
  //========================================================================

     /*
       Inputs:
         EthernetFramesTxIn = Some(m) such that:
          m.malformedFrame == true
          m.frameProtocol == ARP
          ..other fields are irrelevant..

       Expected Outputs:
         EthernetFramesTxOut = None (frame was dropped)
    */
  #[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_14_ARP() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode

    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {frameProtocol: SW::FrameProtocol::ARP, 
      malformedFrame: true, ..Default::default()};

 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(Some(m));

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    // get result values from output ports
    let reply = test_apis::get_EthernetFramesTxOut();

    assert_eq!(reply, None); 
  }

  //========================================================================
  //  (RC_INSPECTA_00-HLR-14) 
  // If the firewall gets a malformed frame, it should drop the frame.
  //========================================================================

     /*
       Inputs:
         EthernetFramesTxIn = Some(m) such that:
          m.malformedFrame == true
          m.internetProtocol == IPv4
          ..other fields are irrelevant..

       Expected Outputs:
         EthernetFramesTxOut = None (frame was dropped)
    */
  #[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_14_IPv4() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode

    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {internetProtocol: SW::InternetProtocol::IPV4, 
      malformedFrame: true, ..Default::default()};

 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(Some(m));

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    // get result values from output ports
    let reply = test_apis::get_EthernetFramesTxOut();

    assert_eq!(reply, None); 
  }

  //This test is a sanity check that intentionally fails
  // provided that we are dropping the malformed IPv4 frame
  // as specified in HLR-14
  /*#[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_14_IPv4_Fail() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode

    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {internetProtocol: SW::InternetProtocol::IPV4, 
      malformedFrame: true, ..Default::default()};

 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(Some(m));

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    // get result values from output ports
    let reply = test_apis::get_EthernetFramesTxOut();

    assert_ne!(reply, None); 
  }*/

  //This test is a sanity check that intentionally fails
  // provided that we are dropping a malformed ARP frame
  // as specified in HLR-14
  /*#[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_14_ARP_Fail() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode

    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {frameProtocol: SW::FrameProtocol::ARP, 
      malformedFrame: true, ..Default::default()};

 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(Some(m));

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    // get result values from output ports
    let reply = test_apis::get_EthernetFramesTxOut();

    assert_ne!(reply, None); 
  }*/

  //========================================================================
  // (RC_INSPECTA_00-HLR-16) 
  // If the firewall gets no input on TxIn, 
  // it should produce no output on TxOut
  //========================================================================

     /*
       Inputs:
         EthernetFramesTxIn = None

       Expected Outputs:
         EthernetFramesTxOut = None (nothing to inspect)
    */
  #[test]
  #[serial]
  fn test_compute_REQ_INSPECTA_HLR_16() {
    // [InvokeEntryPoint]: invoke the entry point test method
    crate::FirewallTx_FirewallTx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: baseline tests run in Normal mode
 
    // [PutInPorts]: put values on the input ports
    test_apis::put_EthernetFramesTxIn(None);

    // [InvokeEntryPoint]: Invoke the entry point
    crate::FirewallTx_FirewallTx_timeTriggered();

    // get result values from output ports
    let reply = test_apis::get_EthernetFramesTxOut();

    assert_eq!(reply, None);

    
  }
}

// CR-01 tests: mode gate and geofence-mock attack detection.
mod cr01_tests {
  use serial_test::serial;

  use crate::test::util::*;
  use data::*;

  // A frame TX passes in Normal mode (well-formed IPv4), with a
  // non-violating payload (byte 0 != 0).
  fn passable_frame() -> SW::StructuredEthernetMessage_i {
    SW::StructuredEthernetMessage_i {
      internetProtocol: SW::InternetProtocol::IPV4,
      malformedFrame: false,
      rawMessage: [50; SW::SW_RawEthernetMessage_DIM_0],
      ..Default::default()
    }
  }

  // Same frame but with the mocked geofence violation (byte 0 == 0).
  fn geofence_frame() -> SW::StructuredEthernetMessage_i {
    let mut raw = [50; SW::SW_RawEthernetMessage_DIM_0];
    raw[0] = 0;
    SW::StructuredEthernetMessage_i { rawMessage: raw, ..passable_frame() }
  }

  // One dispatch without re-initializing (for cross-dispatch transience tests).
  fn dispatch(mode: SW::Mode, input: Option<SW::StructuredEthernetMessage_i>) -> Option<SW::StructuredEthernetMessage_i> {
    test_apis::put_CurrentMode(mode);
    test_apis::put_EthernetFramesTxIn(input);
    crate::FirewallTx_FirewallTx_timeTriggered();
    test_apis::get_EthernetFramesTxOut()
  }

  #[test]
  #[serial]
  fn test_CR01_Tx_Init_initialize() {
    // FirewallTx_Req_Init: attack-status DataPort initialized OK.
    crate::FirewallTx_FirewallTx_initialize();
    assert_eq!(test_apis::get_AttackStatusTx(), SW::AttackStatus::OK);
  }

  #[test]
  #[serial]
  fn test_notify_unknown_channel() {
    // coverage: the notify entry point logs and ignores unknown channels
    crate::FirewallTx_FirewallTx_initialize();
    crate::FirewallTx_FirewallTx_notify(9999);
  }

  #[test]
  #[serial]
  fn test_CR01_Tx_ModeGate_init_drops_passable_frame() {
    // FirewallTx_Req_ModeGate: even a passable frame is dropped in Init.
    crate::FirewallTx_FirewallTx_initialize();
    let out = dispatch(SW::Mode::Init, Some(passable_frame()));
    assert!(out.is_none(), "Init mode must drop every frame");
  }

  #[test]
  #[serial]
  fn test_CR01_Tx_ModeGate_rtl_drops_passable_frame() {
    crate::FirewallTx_FirewallTx_initialize();
    let out = dispatch(SW::Mode::RTL, Some(passable_frame()));
    assert!(out.is_none(), "RTL mode must drop every frame");
  }

  #[test]
  #[serial]
  fn test_CR01_Tx_Detect_geofence_violation_reports_attack() {
    // FirewallTx_Req_Detect: rawMessage[0] == 0 reports Attack
    // (change-plan §9 acceptance criterion 3).
    crate::FirewallTx_FirewallTx_initialize();
    dispatch(SW::Mode::Normal, Some(geofence_frame()));
    assert_eq!(test_apis::get_AttackStatusTx(), SW::AttackStatus::Attack);
  }

  #[test]
  #[serial]
  fn test_CR01_Tx_Detect_is_per_dispatch_transient() {
    // The TX report is per-dispatch: Attack on the violating dispatch, OK
    // again afterwards (persistence lives in the ModeManager's RTL latch —
    // requirements.md Req_Detect_Tx).
    crate::FirewallTx_FirewallTx_initialize();
    dispatch(SW::Mode::Normal, Some(geofence_frame()));
    assert_eq!(test_apis::get_AttackStatusTx(), SW::AttackStatus::Attack);

    dispatch(SW::Mode::Normal, Some(passable_frame()));
    assert_eq!(test_apis::get_AttackStatusTx(), SW::AttackStatus::OK,
      "non-violating dispatch returns to OK");

    dispatch(SW::Mode::Normal, None);
    assert_eq!(test_apis::get_AttackStatusTx(), SW::AttackStatus::OK,
      "no-input dispatch reports OK");
  }

  #[test]
  #[serial]
  fn test_CR01_Tx_Detect_mode_independent() {
    // Detection is observational: the geofence frame is dropped in RTL but
    // still reported (conops §9 Assumption 7).
    crate::FirewallTx_FirewallTx_initialize();
    let out = dispatch(SW::Mode::RTL, Some(geofence_frame()));
    assert!(out.is_none(), "RTL drops the frame");
    assert_eq!(test_apis::get_AttackStatusTx(), SW::AttackStatus::Attack,
      "detection still reports in RTL");
  }

  #[test]
  #[serial]
  fn test_CR01_Tx_Detect_only_byte_zero_triggers() {
    // Only byte 0 is the geofence indicator: zeros elsewhere must not trigger.
    crate::FirewallTx_FirewallTx_initialize();
    let mut raw = [50u8; SW::SW_RawEthernetMessage_DIM_0];
    raw[1] = 0;
    raw[1599] = 0;
    let m = SW::StructuredEthernetMessage_i { rawMessage: raw, ..passable_frame() };
    dispatch(SW::Mode::Normal, Some(m));
    assert_eq!(test_apis::get_AttackStatusTx(), SW::AttackStatus::OK,
      "zeros in bytes 1..1600 are not the geofence indicator");
  }
}

mod GUMBOX_tests {
  use serial_test::serial;
  use proptest::prelude::*;

  use crate::test::util::*;
  use crate::testInitializeCB_macro;
  use crate::testComputeCB_macro;

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

  mod GUMBOX_manual_tests {
  use serial_test::serial;
 
  use crate::test::util::*;
  use data::*;

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_REQ_INSPECTA_HLR_7() {
    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {frameProtocol: SW::FrameProtocol::ARP, malformedFrame: false,
       ..Default::default() };

    let harness_result = 
       cb_apis::testComputeCB(Some(m), SW::Mode::Normal);

    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_REQ_INSPECTA_HLR_12() {
    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {internetProtocol: SW::InternetProtocol::IPV4, malformedFrame: false,
       ..Default::default() };

    let harness_result = 
       cb_apis::testComputeCB(Some(m), SW::Mode::Normal);

    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_REQ_INSPECTA_HLR_14_ARP() {
    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {malformedFrame: true, frameProtocol: SW::FrameProtocol::ARP, ..Default::default() };

    let harness_result = 
       cb_apis::testComputeCB(Some(m), SW::Mode::Normal);

    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_REQ_INSPECTA_HLR_14_IPv4() {
    // generate values for the incoming data ports
    let m = SW::StructuredEthernetMessage_i {malformedFrame: true, internetProtocol: SW::InternetProtocol::IPV4,
       ..Default::default() };

    let harness_result = 
       cb_apis::testComputeCB(Some(m), SW::Mode::Normal);

    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_REQ_INSPECTA_HLR_16() {
    let harness_result = 
       cb_apis::testComputeCB(None, SW::Mode::Normal);

    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
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
    api_EthernetFramesTxIn: generators::option_strategy_default(generators::SW_StructuredEthernetMessage_i_strategy_default()),
    // CR-01: mode input (uniform over Init/Normal/RTL)
    api_CurrentMode: generators::SW_Mode_strategy_default()
  }
}

//============================================================================
//  Specification Audit Tests (/audit-gumbo-contracts, full mode, CR-01)
//
//  These tests probe the SPECIFICATION directly by evaluating the generated
//  GUMBOX oracle functions on constructed pre/post-state pairs — they never
//  invoke the implementation (no test_apis / cb_apis).
//
//  The spec-only audit scored zero findings; the audit_A*/audit_R* probes
//  below back that verdict (A* = oracle accepts intended behavior,
//  R* = oracle rejects wrong behavior). The full-mode pass additionally
//  found ONE genuine defect, demonstrated by the audit_F1* tests:
//
//  F1 — the woven GUMBOX oracle for RC_INSPECTA_00_HLR_14 is WEAKER than the
//  model contract. GUMBO source antecedent:
//      (not isIPV4 and not isARP) | isMalformedFrame
//  emitted Rust (FirewallTx_FirewallTx_GUMBOX.rs):
//      !(isIPV4(..)) && !(isARP(..)) | isMalformedFrame(..)
//  In Rust, `|` binds TIGHTER than `&&`, so this regroups as
//      !isIPV4 && (!isARP | isMalformed)
//  For a malformed IPv4 frame the antecedent is false, so the oracle imposes
//  no drop obligation — the full CEP_Post ACCEPTS forwarding a malformed IPv4
//  frame in Normal mode, an execution the contract text, the woven Verus
//  ensures (which use `||` and group correctly), and the implementation all
//  forbid. Per the audit skill, each audit_F1* test PASSES: a passing test
//  demonstrates that the (oracle-level) specification accepts the problematic
//  scenario. See reports/CR01-specification-audit-FirewallTx.md, Finding F1.
//
//  Argument order for compute_CEP_Post:
//  (api_EthernetFramesTxIn, api_CurrentMode, api_EthernetFramesTxOut,
//   api_AttackStatusTx).
//============================================================================
mod specification_audit_tests {
  use serial_test::serial;
  use crate::bridge::FirewallTx_FirewallTx_GUMBOX as GUMBOX;
  use data::*;

  const OK: SW::AttackStatus = SW::AttackStatus::OK;
  const ATTACK: SW::AttackStatus = SW::AttackStatus::Attack;
  const INIT: SW::Mode = SW::Mode::Init;
  const NORMAL: SW::Mode = SW::Mode::Normal;
  const RTL: SW::Mode = SW::Mode::RTL;

  // Frame constructor with every field explicit (respect the data invariant:
  // TCP => arpType NA, ARP => arpType REQUEST/REPLY).
  fn make_frame(
    malformed: bool,
    ip: SW::InternetProtocol,
    proto: SW::FrameProtocol,
    wl: bool,
    arp: SW::ARP_Type,
    byte0: u8) -> SW::StructuredEthernetMessage_i
  {
    let mut raw = [50u8; SW::SW_RawEthernetMessage_DIM_0];
    raw[0] = byte0;
    SW::StructuredEthernetMessage_i {
      malformedFrame: malformed,
      internetProtocol: ip,
      frameProtocol: proto,
      portIsWhitelisted: wl,
      arpType: arp,
      rawMessage: raw,
    }
  }

  // Well-formed IPv4/TCP frame, non-violating payload (byte 0 = 50).
  fn clean_ipv4() -> SW::StructuredEthernetMessage_i {
    make_frame(false, SW::InternetProtocol::IPV4, SW::FrameProtocol::TCP, true,
      SW::ARP_Type::NA, 50)
  }

  // Well-formed ARP frame.
  fn clean_arp() -> SW::StructuredEthernetMessage_i {
    make_frame(false, SW::InternetProtocol::IPV4, SW::FrameProtocol::ARP, true,
      SW::ARP_Type::REQUEST, 50)
  }

  // ---- acceptance probes: intended behaviors satisfy the oracle ----

  #[test]
  #[serial]
  fn audit_A1_normal_arp_pass_accepted() {
    // Partition row "input, Normal, well-formed, ARP" (HLR_7)
    assert!(GUMBOX::compute_CEP_Post(Some(clean_arp()), NORMAL, Some(clean_arp()), OK),
      "Normal-mode pass of a well-formed ARP frame must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A2_rtl_drops_but_detects_geofence_accepted() {
    // Mode-independent detection: dropped in RTL, still reported (CR01_Tx_Detect)
    let geo = make_frame(false, SW::InternetProtocol::IPV4, SW::FrameProtocol::TCP,
      true, SW::ARP_Type::NA, 0);
    assert!(GUMBOX::compute_CEP_Post(Some(geo), RTL, None, ATTACK),
      "RTL drop with geofence detection must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A3_no_input_no_output_accepted() {
    // Partition row "no input" (HLR_16) + Detect None => OK
    assert!(GUMBOX::compute_CEP_Post(None, INIT, None, OK),
      "no-input dispatch with no output and OK status must satisfy the contract");
  }

  // ---- rejection probes: wrong behaviors violate the oracle ----

  #[test]
  #[serial]
  fn audit_R1_pass_in_rtl_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(Some(clean_ipv4()), RTL, Some(clean_ipv4()), OK),
      "CR01_Tx_ModeGate must reject forwarding in RTL mode");
  }

  #[test]
  #[serial]
  fn audit_R2_geofence_reported_ok_rejected() {
    let geo = make_frame(false, SW::InternetProtocol::IPV4, SW::FrameProtocol::TCP,
      true, SW::ARP_Type::NA, 0);
    assert!(!GUMBOX::compute_CEP_Post(Some(geo), NORMAL, Some(geo), OK),
      "CR01_Tx_Detect must reject OK on a geofence-violating dispatch");
  }

  #[test]
  #[serial]
  fn audit_R3_clean_frame_reported_attack_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(Some(clean_ipv4()), NORMAL, Some(clean_ipv4()), ATTACK),
      "CR01_Tx_Detect must reject Attack on a non-violating dispatch");
  }

  #[test]
  #[serial]
  fn audit_R4_wellformed_arp_dropped_in_normal_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(Some(clean_arp()), NORMAL, None, OK),
      "RC_INSPECTA_00_HLR_7 (MustSend) must reject dropping a well-formed ARP frame in Normal");
  }

  #[test]
  #[serial]
  fn audit_R5_modified_forward_rejected() {
    // AP-2 shape: output differs from input in one raw byte
    let modified = make_frame(false, SW::InternetProtocol::IPV4,
      SW::FrameProtocol::TCP, true, SW::ARP_Type::NA, 51);
    assert!(!GUMBOX::compute_CEP_Post(Some(clean_ipv4()), NORMAL, Some(modified), OK),
      "RC_INSPECTA_00_HLR_12 (output == input) must reject a modified forward");
  }

  #[test]
  #[serial]
  fn audit_R6_fabricated_output_rejected() {
    // AP-3 shape: output with no input
    assert!(!GUMBOX::compute_CEP_Post(None, NORMAL, Some(clean_ipv4()), OK),
      "RC_INSPECTA_00_HLR_16 must reject fabricating output with no input");
  }

  #[test]
  #[serial]
  fn audit_R7_wellformed_ipv6_tcp_forwarded_rejected() {
    // HLR_14's oracle is still correct in the non-IPv4 region
    let v6 = make_frame(false, SW::InternetProtocol::IPV6, SW::FrameProtocol::TCP,
      true, SW::ARP_Type::NA, 50);
    assert!(!GUMBOX::compute_CEP_Post(Some(v6), NORMAL, Some(v6), OK),
      "RC_INSPECTA_00_HLR_14 must reject forwarding a well-formed IPv6 non-ARP frame");
  }

  // ---- F1 demonstration tests (each PASSES, demonstrating the oracle gap) ----

  #[test]
  #[serial]
  fn audit_F1a_oracle_accepts_malformed_ipv4_forward_clause_level() {
    // SPEC WEAKNESS (oracle-level): the HLR_14 clause oracle imposes nothing
    // on a malformed IPv4 frame — the regrouped antecedent !IPv4 && (...) is
    // false — so forwarding it is accepted. The GUMBO contract requires NoSend.
    let mal4 = make_frame(true, SW::InternetProtocol::IPV4, SW::FrameProtocol::TCP,
      true, SW::ARP_Type::NA, 50);
    assert!(GUMBOX::compute_spec_RC_INSPECTA_00_HLR_14_guarantee(Some(mal4), Some(mal4)),
      "demonstrates F1: HLR_14 oracle accepts forwarding a malformed IPv4 frame");
  }

  #[test]
  #[serial]
  fn audit_F1b_oracle_accepts_malformed_ipv4_forward_full_post() {
    // SPEC WEAKNESS (oracle-level): the COMPLETE compute oracle accepts an
    // execution the Verus-verified implementation can never produce —
    // forwarding a malformed IPv4 frame in Normal mode. Every GUMBOX-based
    // test (manual CB + PropTest) inherits this blind spot.
    let mal4 = make_frame(true, SW::InternetProtocol::IPV4, SW::FrameProtocol::TCP,
      true, SW::ARP_Type::NA, 50);
    assert!(GUMBOX::compute_CEP_Post(Some(mal4), NORMAL, Some(mal4), OK),
      "demonstrates F1: full oracle accepts forwarding a malformed IPv4 frame in Normal mode");
  }

  #[test]
  #[serial]
  fn audit_F1c_contrast_malformed_ipv6_arp_still_rejected() {
    // Contrast probe: for a malformed IPv6 ARP frame the regrouped antecedent
    // is still true, so the oracle correctly demands the drop — the divergence
    // is exactly the isIPV4 conjunct's lost grouping.
    let mal6arp = make_frame(true, SW::InternetProtocol::IPV6, SW::FrameProtocol::ARP,
      true, SW::ARP_Type::REQUEST, 50);
    assert!(!GUMBOX::compute_spec_RC_INSPECTA_00_HLR_14_guarantee(Some(mal6arp), Some(mal6arp)),
      "F1 contrast: HLR_14 oracle still rejects forwarding a malformed IPv6 ARP frame");
  }

  // ---- initialize probes ----

  #[test]
  #[serial]
  fn audit_A4_initialize_accepted() {
    assert!(GUMBOX::initialize_IEP_Post(None, OK),
      "(status OK) must satisfy CR01_Tx_Init");
  }

  #[test]
  #[serial]
  fn audit_R8_initialize_attack_status_rejected() {
    assert!(!GUMBOX::initialize_IEP_Post(None, ATTACK),
      "CR01_Tx_Init must reject an initial Attack status");
  }
}
