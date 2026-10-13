// This file will not be overwritten if codegen is rerun

use data::*;
use crate::bridge::FirewallTx_FirewallTx_api::*;
use vstd::prelude::*;

verus! {

  pub struct FirewallTx_FirewallTx {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl FirewallTx_FirewallTx {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: FirewallTx_FirewallTx_Put_Api> (
      &mut self,
      api: &mut FirewallTx_FirewallTx_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee CR01_Tx_Init
        //   FirewallTx_Req_Init: attack status DataPort initialized to OK.
        final(api).AttackStatusTx == SW::AttackStatus::OK,
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");

      // CR-01 FirewallTx_Req_Init: initialize the attack-status DataPort to OK.
      api.put_AttackStatusTx(SW::AttackStatus::OK);
    }

    pub fn timeTriggered<API: FirewallTx_FirewallTx_Full_Api> (
      &mut self,
      api: &mut FirewallTx_FirewallTx_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).EthernetFramesTxOut.is_none(),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee RC_INSPECTA_00_HLR_7
        //   2.1 firewall: copy out TxIn arp frame (RC_INSPECTA_00-HLR-7; revised CR-01: applies in Normal mode only) In Normal mode, if the firewall gets a wellformed Arp frame from TxIn, the firewall shall copy the frame to TxOut.
        final(api).EthernetFramesTxIn.is_some() ==>
          (((final(api).CurrentMode == SW::Mode::Normal) &&
            !(GumboLib::isMalformedFrame_spec(final(api).EthernetFramesTxIn.unwrap()))) &&
            GumboLib::isARP_spec(final(api).EthernetFramesTxIn.unwrap())) ==>
            final(api).EthernetFramesTxOut.is_some() &&
              (final(api).EthernetFramesTxIn.unwrap() == final(api).EthernetFramesTxOut.unwrap()),
        // guarantee RC_INSPECTA_00_HLR_12
        //   2.2 firewall: copy out TxIn ipv4 frame (RC_INSPECTA_00-HLR-12; revised CR-01: applies in Normal mode only) In Normal mode, if the firewall gets a wellformed IPv4 frame from TxIn, the firewall shall copy the frame to TxOut.
        final(api).EthernetFramesTxIn.is_some() ==>
          (((final(api).CurrentMode == SW::Mode::Normal) &&
            !(GumboLib::isMalformedFrame_spec(final(api).EthernetFramesTxIn.unwrap()))) &&
            GumboLib::isIPV4_spec(final(api).EthernetFramesTxIn.unwrap())) ==>
            final(api).EthernetFramesTxOut.is_some() &&
              (final(api).EthernetFramesTxIn.unwrap() == final(api).EthernetFramesTxOut.unwrap()),
        // guarantee RC_INSPECTA_00_HLR_14
        //   2.3 firewall: do not copy disallowed frame (RC_INSPECTA_00-HLR-14) If the firewall gets a malformed ARP frame or malformed TCP frame, it should drop the frame.
        final(api).EthernetFramesTxIn.is_some() ==>
          (!(GumboLib::isIPV4_spec(final(api).EthernetFramesTxIn.unwrap())) && !(GumboLib::isARP_spec(final(api).EthernetFramesTxIn.unwrap())) ||
            GumboLib::isMalformedFrame_spec(final(api).EthernetFramesTxIn.unwrap())) ==>
            final(api).EthernetFramesTxOut.is_none(),
        // guarantee RC_INSPECTA_00_HLR_16
        //   2.4 firewall: no output on empty input (RC_INSPECTA_00-HLR-16) If the firewall gets no input on TxIn, it should produce no output on TxOut
        !(final(api).EthernetFramesTxIn.is_some()) ==> final(api).EthernetFramesTxOut.is_none(),
        // guarantee CR01_Tx_ModeGate
        //   FirewallTx_Req_ModeGate (CR-01): in Init and RTL modes, drop every frame — no output regardless of input.
        !(final(api).CurrentMode == SW::Mode::Normal) ==> final(api).EthernetFramesTxOut.is_none(),
        // guarantee CR01_Tx_Detect
        //   FirewallTx_Req_Detect (CR-01): report Attack on any dispatch whose received frame carries the mocked geofence violation (rawMessage byte 0 == 0), OK on every other dispatch; mode-independent, per-dispatch (no latch — persistence is the ModeManager's RTL).
        (final(api).EthernetFramesTxIn.is_some() && GumboLib::isGeofenceViolation_spec(final(api).EthernetFramesTxIn.unwrap()) ==>
          (final(api).AttackStatusTx == SW::AttackStatus::Attack)) &&
          (!(final(api).EthernetFramesTxIn.is_some()) || !(GumboLib::isGeofenceViolation_spec(final(api).EthernetFramesTxIn.unwrap())) ==>
            (final(api).AttackStatusTx == SW::AttackStatus::OK)),
        // END MARKER TIME TRIGGERED ENSURES
    {
      log_info("compute entrypoint invoked");

      // -------------- Get values of input ports ------------------
      let mode = api.get_CurrentMode();
      let ethernet_frame: Option<SW::StructuredEthernetMessage_i> = api.get_EthernetFramesTxIn();

      // CR-01 FirewallTx_Req_Detect: per-dispatch, mode-independent
      // geofence-mock detection (rawMessage byte 0 == 0).
      let geofence_violation: bool = match ethernet_frame {
        Some(frame) => frame.rawMessage[0] == 0u8,
        None => false,
      };
      if geofence_violation {
        api.put_AttackStatusTx(SW::AttackStatus::Attack);
        log_geofence_attack();
      } else {
        api.put_AttackStatusTx(SW::AttackStatus::OK);
      }

      // CR-01 FirewallTx_Req_ModeGate: frames flow only in Normal mode.
      // The Normal-mode branch is the unmodified baseline mediation logic.
      match mode {
        SW::Mode::Normal => {
          match ethernet_frame {
            Some(frame) => {
              if (!frame.malformedFrame)
              {
                match frame.frameProtocol {
                    //RC_INSPECTA_00_HLR_7
                    SW::FrameProtocol::ARP => {
                      api.put_EthernetFramesTxOut(frame);
                    },
                    _ => {
                      match frame.internetProtocol {
                        //RC_INSPECTA_00_HLR_12
                        SW::InternetProtocol::IPV4 => {
                          api.put_EthernetFramesTxOut(frame);
                        }
                        //RC_INSPECTA_00_HLR_14
                        _ => {}
                      };
                    },
                };
              } else {
                //RC_INSPECTA_00_HLR_14
                //Drop the malformed packet/send nothing.
              }
            },
            //RC_INSPECTA_00_HLR_16
            _ => {}
          };
        },
        _ => {
          // CR01_Tx_ModeGate: Init/RTL — drop every frame
        }
      }
    }

    pub fn notify(
      &mut self,
      channel: microkit_channel)
    {
      // this method is called when the monitor does not handle the passed in channel
      match channel {
        _ => {
          log_warn_channel(channel)
        }
      }
    }
  }

  #[verifier::external_body]
  pub fn log_info(msg: &str)
  {
    log::info!("{0}", msg);
  }

  #[verifier::external_body]
  pub fn log_warn_channel(channel: u32)
  {
    log::warn!("Unexpected channel: {0}", channel);
  }

  // CR-01: logging method for detected geofence violations.
  #[verifier::external_body]
  pub fn log_geofence_attack()
  {
    log::info!("Tx Firewall: geofence violation detected (rawMessage[0] == 0) - reporting Attack");
  }

  // BEGIN MARKER GUMBO METHODS
  pub open spec fn isMalformedFrame(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.malformedFrame
  }

  pub open spec fn getInternetProtocol(v: SW::StructuredEthernetMessage_i) -> SW::InternetProtocol
  {
    v.internetProtocol
  }

  pub open spec fn isIPV4(v: SW::StructuredEthernetMessage_i) -> bool
  {
    getInternetProtocol(v) == SW::InternetProtocol::IPV4
  }

  pub open spec fn isIPV6(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.internetProtocol == SW::InternetProtocol::IPV6
  }

  pub open spec fn getFrameProtocol(v: SW::StructuredEthernetMessage_i) -> SW::FrameProtocol
  {
    v.frameProtocol
  }

  pub open spec fn isTCP(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.frameProtocol == SW::FrameProtocol::TCP
  }

  pub open spec fn isARP(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.frameProtocol == SW::FrameProtocol::ARP
  }

  pub open spec fn isPortWhitelisted(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.portIsWhitelisted
  }

  pub open spec fn getARP_Type(v: SW::StructuredEthernetMessage_i) -> SW::ARP_Type
  {
    v.arpType
  }

  pub open spec fn isARP_Request(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.arpType == SW::ARP_Type::REQUEST
  }

  pub open spec fn isARP_Reply(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.arpType == SW::ARP_Type::REPLY
  }
  // END MARKER GUMBO METHODS

}
