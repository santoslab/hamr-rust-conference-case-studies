// This file will not be overwritten if codegen is rerun

use data::SW;

use crate::test::util::test_apis;

mod tests {
  // NOTE: need to run tests sequentially to prevent race conditions
  //       on the app and the testing apis which are static
  use serial_test::serial;

  use crate::test::{self, util::*};
  use data::*;

  #[test]
  #[serial]
  fn test_initialization() {
    crate::FirewallRx_FirewallRx_initialize();
  }

  #[test]
  #[serial]
  fn test_compute() {
    crate::FirewallRx_FirewallRx_initialize();
    test_apis::put_CurrentMode(SW::Mode::Normal); // CR-01: mode DataPort must be set before dispatch
    crate::FirewallRx_FirewallRx_timeTriggered();
  }

  // Helper function for: Initalizing FirewallRx_FirewallRx and its get/set apis functions.
  // CR-01 re-scope: the baseline HLR tests exercise Normal-mode behavior, so the
  // helper now samples mode Normal (change-plan R1: baseline suites re-run under
  // mode=Normal must pass unchanged).
  fn run_rx_firewall(input: Option<SW::StructuredEthernetMessage_i>) -> Option<SW::StructuredEthernetMessage_i>
  {
    run_rx_firewall_in_mode(SW::Mode::Normal, input)
  }

  // CR-01: same, with an explicit mode.
  fn run_rx_firewall_in_mode(mode: SW::Mode, input: Option<SW::StructuredEthernetMessage_i>) -> Option<SW::StructuredEthernetMessage_i>
  {
    crate::FirewallRx_FirewallRx_initialize();
    test_apis::put_CurrentMode(mode);
    test_apis::put_EthernetFramesRxIn(input);
    crate::FirewallRx_FirewallRx_timeTriggered();
    test_apis::get_EthernetFramesRxOut()
  }

  #[test]
  #[serial]
  fn test_RC_INSPECTA_00_HLR_1_no_input()                            // Manual unit test for No input frames implies no output frames.
  {
    let output = run_rx_firewall(None);
    assert!(output.is_none(), "No input on RxIn should not pass any frame");
  }

  #[test]
  #[serial]
  fn test_RC_INSPECTA_00_HLR_2_drop_malformed()                      // Manual unit test for properly dropping frames that are malformed.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_TCP_MF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: true,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let output = run_rx_firewall(Some(IPv4_TCP_MF_WL_ARPNA));

    assert!(output.is_none(), "Frame with undefined port should be dropped");
  }

  #[test]
  #[serial]
  fn test_RC_INSPECTA_00_HLR_4_drop_ipv6()                          // Manual unit test for properly dropping IPV6 frames.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv6_TCP_NotMF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV6,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };
    let IPv6_ARP_NotMF_WL_ARPREQUEST = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV6,
      frameProtocol: SW::FrameProtocol::ARP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::REQUEST,
      rawMessage: test_message,
    };

    let output_1 = run_rx_firewall(Some(IPv6_TCP_NotMF_WL_ARPNA));
    let output_2 = run_rx_firewall(Some(IPv6_ARP_NotMF_WL_ARPREQUEST));

    assert!(output_1.is_none(), "IPV6 frame should be dropped");
    assert!(output_2.is_none(), "IPV6 frame should be dropped");
  }

  #[test]
  #[serial]
  fn test_RC_INSPECTA_00_HLR_6_drop_ARP()                           // Manual unit test for properly dropping frames with ARP protocol.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_ARP_NotMF_WL_ARPREQUEST = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::ARP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::REQUEST,
      rawMessage: test_message,
    };
    let IPv4_ARP_NotMF_WL_ARPREPLY = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::ARP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::REPLY,
      rawMessage: test_message,
    };
    let IPv4_ARP_NotMF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::ARP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let output_1 = run_rx_firewall(Some(IPv4_ARP_NotMF_WL_ARPREQUEST));
    let output_2 = run_rx_firewall(Some(IPv4_ARP_NotMF_WL_ARPREPLY));
    let output_3 = run_rx_firewall(Some(IPv4_ARP_NotMF_WL_ARPNA));

    assert!(output_1.is_none(), "ARP frame should be dropped");
    assert!(output_2.is_none(), "ARP frame should be dropped");
    assert!(output_3.is_none(), "ARP frame should be dropped");
  }

  #[test]
  #[serial]
  fn test_RC_INSPECTA_00_HLR_6_ARP_type()                           // Manual unit test for no change in RxOut frame no matter the ARP type.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let arp_types = vec![
      SW::ARP_Type::REQUEST,
      SW::ARP_Type::REPLY,
      SW::ARP_Type::NA
    ];
    
    for arp_type in arp_types
    {
      let IPv4_ARP_NotMF_WL = SW::StructuredEthernetMessage_i {
        malformedFrame: false,
        internetProtocol: SW::InternetProtocol::IPV4,
        frameProtocol: SW::FrameProtocol::ARP,
        portIsWhitelisted: true,
        arpType: arp_type,
        rawMessage: test_message,
      };

      let output = run_rx_firewall(Some(IPv4_ARP_NotMF_WL));
      assert!(output.is_none(), "ARP type should not change message dropping");
    }
  }

  #[test]
  #[serial]
  fn test_RC_INSPECTA_00_HLR_8_drop_undefined_whitelist_port()      // Manual unit test for properly dropping frames with undefined whitelist port.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_ARP_NotMF_NoWL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: false,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let output_1 = run_rx_firewall(Some(IPv4_ARP_NotMF_NoWL_ARPNA));

    assert!(output_1.is_none(), "Frame with undefined port should be dropped");
  }

  #[test]
  #[serial]
  fn test_RC_INSPECTA_00_HLR_9_pass_defined_port()                  // Manual unit test for properly passing IPV4 frames with - TCP protocol and port defined. 
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_TCP_NotMF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let output = run_rx_firewall(Some(IPv4_TCP_NotMF_WL_ARPNA));

    assert!(output.is_some(), "Frame with undefined port should be dropped");
  }

  #[test]
  #[serial]
  fn test_integration_properties()                                  // Manual unit test for checking all integration properties of frames in RxIn.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let internet_protocols = vec![
      SW::InternetProtocol::IPV4,
      SW::InternetProtocol::IPV6
    ];

    let frame_protocols = vec![
      SW::FrameProtocol::TCP,
      SW::FrameProtocol::ARP
    ];

    let boolean = vec![
      true,
      false,
    ];
    
    for internet_portocol in internet_protocols
    {
      for frame_protocol in frame_protocols.clone()
      {
        for isWhitelisted in boolean.clone()
        {
          let frame = SW::StructuredEthernetMessage_i {
            malformedFrame: true,
            internetProtocol: internet_portocol,
            frameProtocol: frame_protocol,
            portIsWhitelisted: isWhitelisted,
            arpType: SW::ARP_Type::NA,
            rawMessage: test_message,
          };
          let output = run_rx_firewall(Some(frame));
          
          assert!(!matches!(output, Some(ref o) if o.internetProtocol == SW::InternetProtocol::IPV6)
            , "IPV6 frame should be dropped");
          assert!(!matches!(output, Some(ref o) if o.internetProtocol == SW::InternetProtocol::IPV4 &&
            o.frameProtocol == SW::FrameProtocol::TCP && o.portIsWhitelisted == false)
            , "Frame with undefined port should be dropped");
          assert!(!matches!(output, Some(ref o) if o.internetProtocol == SW::InternetProtocol::IPV4 &&
            o.frameProtocol == SW::FrameProtocol::ARP)
            , "ARP frame should be dropped");
        }
      }
    }
  }
}

// CR-01 tests: mode gate, malformed-frame counting, attack detection.
mod cr01_tests {
  use serial_test::serial;

  use crate::test::util::*;
  use data::*;

  // An allowed frame: in Normal mode this must pass (RC_INSPECTA_00_HLR_9).
  fn allowed_frame() -> SW::StructuredEthernetMessage_i {
    SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: [0; 1600],
    }
  }

  fn malformed_frame() -> SW::StructuredEthernetMessage_i {
    SW::StructuredEthernetMessage_i { malformedFrame: true, ..allowed_frame() }
  }

  // One dispatch without re-initializing (for cross-dispatch state tests).
  fn dispatch(mode: SW::Mode, input: Option<SW::StructuredEthernetMessage_i>) -> Option<SW::StructuredEthernetMessage_i> {
    test_apis::put_CurrentMode(mode);
    test_apis::put_EthernetFramesRxIn(input);
    crate::FirewallRx_FirewallRx_timeTriggered();
    test_apis::get_EthernetFramesRxOut()
  }

  #[test]
  #[serial]
  fn test_CR01_Rx_Init_initialize() {
    // FirewallRx_Req_Init: count 0, attack-status DataPort initialized OK.
    crate::FirewallRx_FirewallRx_initialize();
    assert_eq!(test_apis::get_malformedCount(), 0);
    assert_eq!(test_apis::get_AttackStatusRx(), SW::AttackStatus::OK);
  }

  #[test]
  #[serial]
  fn test_notify_unknown_channel() {
    // coverage: the notify entry point logs and ignores unknown channels
    crate::FirewallRx_FirewallRx_initialize();
    crate::FirewallRx_FirewallRx_notify(9999);
  }

  #[test]
  #[serial]
  fn test_CR01_Rx_ModeGate_init_drops_allowed_frame() {
    // FirewallRx_Req_ModeGate: even an allowed frame is dropped in Init.
    crate::FirewallRx_FirewallRx_initialize();
    let out = dispatch(SW::Mode::Init, Some(allowed_frame()));
    assert!(out.is_none(), "Init mode must drop every frame");
  }

  #[test]
  #[serial]
  fn test_CR01_Rx_ModeGate_rtl_drops_allowed_frame() {
    crate::FirewallRx_FirewallRx_initialize();
    let out = dispatch(SW::Mode::RTL, Some(allowed_frame()));
    assert!(out.is_none(), "RTL mode must drop every frame");
  }

  #[test]
  #[serial]
  fn test_CR01_Rx_Count_threshold_and_latch() {
    // FirewallRx_Req_Count / FirewallRx_Req_Detect: OK through the 5th
    // malformed frame, Attack on the 6th (count > 5), latched thereafter,
    // count saturating at 6 (change-plan §9 acceptance criterion 3).
    crate::FirewallRx_FirewallRx_initialize();

    for i in 1..=5 {
      dispatch(SW::Mode::Normal, Some(malformed_frame()));
      assert_eq!(test_apis::get_malformedCount(), i);
      assert_eq!(test_apis::get_AttackStatusRx(), SW::AttackStatus::OK,
        "count {i} <= 5: still OK");
    }

    dispatch(SW::Mode::Normal, Some(malformed_frame()));
    assert_eq!(test_apis::get_malformedCount(), 6);
    assert_eq!(test_apis::get_AttackStatusRx(), SW::AttackStatus::Attack,
      "6th malformed frame: count > 5 reports Attack");

    // latched: well-formed and empty dispatches keep reporting Attack
    dispatch(SW::Mode::Normal, Some(allowed_frame()));
    assert_eq!(test_apis::get_AttackStatusRx(), SW::AttackStatus::Attack);
    dispatch(SW::Mode::Normal, None);
    assert_eq!(test_apis::get_AttackStatusRx(), SW::AttackStatus::Attack);

    // saturation: a 7th malformed frame holds the count at 6
    dispatch(SW::Mode::Normal, Some(malformed_frame()));
    assert_eq!(test_apis::get_malformedCount(), 6, "count saturates at 6");
  }

  #[test]
  #[serial]
  fn test_CR01_Rx_Count_mode_independent() {
    // Detection is observational: counting proceeds while Init mode drops
    // every frame (requirements.md Req_Detect_Rx; conops §9 Assumption 7).
    crate::FirewallRx_FirewallRx_initialize();
    for _ in 0..6 {
      let out = dispatch(SW::Mode::Init, Some(malformed_frame()));
      assert!(out.is_none(), "Init mode drops the frames being counted");
    }
    assert_eq!(test_apis::get_AttackStatusRx(), SW::AttackStatus::Attack,
      "threshold crossed while in Init mode");
  }

  #[test]
  #[serial]
  fn test_CR01_Rx_wellformed_frames_do_not_count() {
    crate::FirewallRx_FirewallRx_initialize();
    for _ in 0..8 {
      dispatch(SW::Mode::Normal, Some(allowed_frame()));
    }
    assert_eq!(test_apis::get_malformedCount(), 0);
    assert_eq!(test_apis::get_AttackStatusRx(), SW::AttackStatus::OK);
  }
}

mod GUMBOX_manual_tests {
  use serial_test::serial;
  
  use crate::test::util::*;
  use data::*;

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_RC_INSPECTA_00_HLR_1()              // GUMBOX unit test for RC_INSPECTA_00_HLR_1 guarantee.
  {
    let harness_result = cb_apis::testComputeCB(None, SW::Mode::Normal);
    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_RC_INSPECTA_00_HLR_2()              // GUMBOX unit test for RC_INSPECTA_00_HLR_2 guarantee.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_TCP_MF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: true,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let harness_result = cb_apis::testComputeCB(Some(IPv4_TCP_MF_WL_ARPNA), SW::Mode::Normal);
    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }
  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_RC_INSPECTA_00_HLR_4()              // GUMBOX unit test for RC_INSPECTA_00_HLR_4 guarantee.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv6_TCP_NotMF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV6,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let harness_result = cb_apis::testComputeCB(Some(IPv6_TCP_NotMF_WL_ARPNA), SW::Mode::Normal);
    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }
  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_RC_INSPECTA_00_HLR_6()              // GUMBOX unit test for RC_INSPECTA_00_HLR_6 guarantee.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_ARP_NotMF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::ARP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let harness_result = cb_apis::testComputeCB(Some(IPv4_ARP_NotMF_WL_ARPNA), SW::Mode::Normal);
    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }
  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_RC_INSPECTA_00_HLR_8()              // GUMBOX unit test for RC_INSPECTA_00_HLR_8 guarantee.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_TCP_NotMF_NoWL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: false,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let harness_result = cb_apis::testComputeCB(Some(IPv4_TCP_NotMF_NoWL_ARPNA), SW::Mode::Normal);
    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
  }

  #[test]
  #[serial]
  fn test_compute_GUMBOX_manual_RC_INSPECTA_00_HLR_9()              // GUMBOX unit test for RC_INSPECTA_00_HLR_9 guarantee.
  {
    let test_message: [u8; 1600] = [0; 1600];

    let IPv4_TCP_NotMF_WL_ARPNA = SW::StructuredEthernetMessage_i {
      malformedFrame: false,
      internetProtocol: SW::InternetProtocol::IPV4,
      frameProtocol: SW::FrameProtocol::TCP,
      portIsWhitelisted: true,
      arpType: SW::ARP_Type::NA,
      rawMessage: test_message,
    };

    let harness_result = cb_apis::testComputeCB(Some(IPv4_TCP_NotMF_WL_ARPNA), SW::Mode::Normal);
    assert!(matches!(harness_result, cb_apis::HarnessResult::Passed));
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
    api_EthernetFramesRxIn: generators::option_strategy_default(generators::SW_StructuredEthernetMessage_i_strategy_default()),
    // CR-01: mode input (uniform over Init/Normal/RTL)
    api_CurrentMode: generators::SW_Mode_strategy_default()
  }

  // CR-01: property-based exploration of the malformedCount state machine
  // (pre-state count set directly, full i32 range — the contract covers all).
  testComputeCBwGSV_macro! {
    prop_testComputeCBwGSV_macro, // test name
    config: ProptestConfig { // proptest configuration, built by overriding fields from default config
      cases: numValidComputeTestCases,
      max_global_rejects: numValidComputeTestCases * computeRejectRatio,
      verbose: verbosity,
      ..ProptestConfig::default()
    },
    // strategies for generating each component input
    In_malformedCount: generators::i32_strategy_default(),
    api_EthernetFramesRxIn: generators::option_strategy_default(generators::SW_StructuredEthernetMessage_i_strategy_default()),
    api_CurrentMode: generators::SW_Mode_strategy_default()
  }
}

//============================================================================
//  Specification Audit Tests (/audit-gumbo-contracts, full mode, CR-01)
//
//  These tests probe the SPECIFICATION directly by evaluating the generated
//  GUMBOX oracle functions on constructed pre/post-state pairs — they never
//  invoke the implementation (no test_apis / cb_apis). The audit scored zero
//  findings (reports/CR01-specification-audit-FirewallRx.md), so these are
//  ADEQUACY PROBES backing that verdict:
//    audit_A*  — the oracle ACCEPTS an intended behavior (assert  Post(...));
//    audit_R*  — the oracle REJECTS a wrong behavior     (assert !Post(...)).
//  Every test passing = the zero-findings verdict is confirmed against the
//  woven oracle, not just the model text. Argument order for compute_CEP_Post:
//  (In_malformedCount, malformedCount, api_EthernetFramesRxIn, api_CurrentMode,
//   api_EthernetFramesRxOut, api_AttackStatusRx).
//============================================================================
mod specification_audit_tests {
  use serial_test::serial;
  use crate::bridge::FirewallRx_FirewallRx_GUMBOX as GUMBOX;
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

  // The RX allow-list frame: well-formed, IPv4, TCP, whitelisted.
  fn allowed() -> SW::StructuredEthernetMessage_i {
    make_frame(false, SW::InternetProtocol::IPV4, SW::FrameProtocol::TCP, true,
      SW::ARP_Type::NA, 50)
  }

  fn malformed() -> SW::StructuredEthernetMessage_i {
    make_frame(true, SW::InternetProtocol::IPV4, SW::FrameProtocol::TCP, true,
      SW::ARP_Type::NA, 50)
  }

  // ---- acceptance probes: intended behaviors satisfy the oracle ----

  #[test]
  #[serial]
  fn audit_A1_normal_allowed_pass_accepted() {
    // Partition row "input, Normal, IPv4·TCP·whitelisted·well-formed" (HLR_9)
    assert!(GUMBOX::compute_CEP_Post(0, 0, Some(allowed()), NORMAL, Some(allowed()), OK),
      "Normal-mode pass of an allowed frame must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A2_init_drop_of_allowed_frame_accepted() {
    // Partition row "input, mode != Normal" (CR01_Rx_ModeGate)
    assert!(GUMBOX::compute_CEP_Post(0, 0, Some(allowed()), INIT, None, OK),
      "Init-mode drop of an allowed frame must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A3_malformed_counted_and_dropped_accepted() {
    // Partition rows HLR_2 (drop) + CR01_Rx_Count (increment)
    assert!(GUMBOX::compute_CEP_Post(0, 1, Some(malformed()), NORMAL, None, OK),
      "counted+dropped malformed frame must satisfy the contract");
  }

  #[test]
  #[serial]
  fn audit_A4_threshold_crossing_reports_attack_accepted() {
    // CR01_Rx_Count (5 -> 6) + CR01_Rx_Detect (post-count > 5 => Attack)
    assert!(GUMBOX::compute_CEP_Post(5, 6, Some(malformed()), NORMAL, None, ATTACK),
      "6th malformed frame reporting Attack must satisfy the contract");
  }

  // ---- rejection probes: wrong behaviors violate the oracle ----

  #[test]
  #[serial]
  fn audit_R1_pass_through_in_init_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(0, 0, Some(allowed()), INIT, Some(allowed()), OK),
      "CR01_Rx_ModeGate must reject forwarding in Init mode");
  }

  #[test]
  #[serial]
  fn audit_R2_allowed_frame_dropped_in_normal_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(0, 0, Some(allowed()), NORMAL, None, OK),
      "RC_INSPECTA_00_HLR_9 (MustSend) must reject dropping an allowed frame in Normal");
  }

  #[test]
  #[serial]
  fn audit_R3_modified_forward_rejected() {
    // AP-2 shape: output differs from input in one raw byte
    let modified = make_frame(false, SW::InternetProtocol::IPV4,
      SW::FrameProtocol::TCP, true, SW::ARP_Type::NA, 51);
    assert!(!GUMBOX::compute_CEP_Post(0, 0, Some(allowed()), NORMAL, Some(modified), OK),
      "RC_INSPECTA_00_HLR_9 (output == input) must reject a modified forward");
  }

  #[test]
  #[serial]
  fn audit_R4_malformed_forwarded_in_normal_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(0, 1, Some(malformed()), NORMAL, Some(malformed()), OK),
      "RC_INSPECTA_00_HLR_2 must reject forwarding a malformed frame");
  }

  #[test]
  #[serial]
  fn audit_R5_missing_count_increment_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(0, 0, Some(malformed()), NORMAL, None, OK),
      "CR01_Rx_Count must reject an unchanged count on a malformed frame below saturation");
  }

  #[test]
  #[serial]
  fn audit_R6_count_increment_on_wellformed_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(0, 1, Some(allowed()), NORMAL, Some(allowed()), OK),
      "CR01_Rx_Count must reject counting a well-formed frame");
  }

  #[test]
  #[serial]
  fn audit_R7_ok_above_threshold_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(6, 6, Some(malformed()), NORMAL, None, OK),
      "CR01_Rx_Detect must reject OK when the post-update count exceeds 5");
  }

  #[test]
  #[serial]
  fn audit_R8_attack_below_threshold_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(0, 0, None, NORMAL, None, ATTACK),
      "CR01_Rx_Detect must reject Attack when the post-update count is <= 5");
  }

  #[test]
  #[serial]
  fn audit_R9_fabricated_output_rejected() {
    // AP-3 shape: output with no input
    assert!(!GUMBOX::compute_CEP_Post(0, 0, None, NORMAL, Some(allowed()), OK),
      "RC_INSPECTA_00_HLR_1 must reject fabricating output with no input");
  }

  #[test]
  #[serial]
  fn audit_R10_count_past_saturation_rejected() {
    assert!(!GUMBOX::compute_CEP_Post(6, 7, Some(malformed()), NORMAL, None, ATTACK),
      "CR01_Rx_Count must reject counting past the saturation bound 6");
  }

  // ---- initialize probes (the oracle pins malformedCount and AttackStatusRx;
  //      the event out-port parameter is unconstrained at initialize, matching
  //      the model: EventDataPort initialization is optional) ----

  #[test]
  #[serial]
  fn audit_A5_initialize_accepted() {
    assert!(GUMBOX::initialize_IEP_Post(0, None, OK),
      "(count 0, status OK) must satisfy CR01_Rx_Init");
  }

  #[test]
  #[serial]
  fn audit_R11_initialize_nonzero_count_rejected() {
    assert!(!GUMBOX::initialize_IEP_Post(1, None, OK),
      "CR01_Rx_Init must reject a non-zero initial malformed count");
  }

  #[test]
  #[serial]
  fn audit_R12_initialize_attack_status_rejected() {
    assert!(!GUMBOX::initialize_IEP_Post(0, None, ATTACK),
      "CR01_Rx_Init must reject an initial Attack status");
  }
}
