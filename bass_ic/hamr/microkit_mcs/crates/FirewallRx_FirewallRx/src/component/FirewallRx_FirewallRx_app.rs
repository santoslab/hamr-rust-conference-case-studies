// This file will not be overwritten if codegen is rerun

use data::{SW::InternetProtocol, *};
use crate::bridge::FirewallRx_FirewallRx_api::*;
use vstd::prelude::*;

verus! {

  pub struct FirewallRx_FirewallRx {
    // BEGIN MARKER STATE VARS
    pub malformedCount: i32,
    // END MARKER STATE VARS
  }

  impl FirewallRx_FirewallRx {
    pub fn new() -> Self
    {
      Self {
        // BEGIN MARKER STATE VAR INIT
        malformedCount: 0,
        // END MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: FirewallRx_FirewallRx_Put_Api> (
      &mut self,
      api: &mut FirewallRx_FirewallRx_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee CR01_Rx_Init
        //   FirewallRx_Req_Init: malformed count starts at zero; attack status DataPort initialized to OK.
        (final(self).malformedCount == 0i32) &&
          (final(api).AttackStatusRx == SW::AttackStatus::OK),
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");

      // CR-01 FirewallRx_Req_Init: zero the malformed count and initialize
      // the attack-status DataPort to OK.
      self.malformedCount = 0;
      api.put_AttackStatusRx(SW::AttackStatus::OK);
    }

    pub fn timeTriggered<API: FirewallRx_FirewallRx_Full_Api> (
      &mut self,
      api: &mut FirewallRx_FirewallRx_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).EthernetFramesRxOut.is_none(),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee RC_INSPECTA_00_HLR_1
        //   1.1 firewall: no frame in RxOut if no frame in RxIn (RC_INSPECTA_00-HLR-1) The firewall shall not have any frame in RxOut if there are no frame in RxIn.
        !(final(api).EthernetFramesRxIn.is_some()) ==> final(api).EthernetFramesRxOut.is_none(),
        // guarantee RC_INSPECTA_00_HLR_2
        //   1.2 firewall: drop malformed frames (RC_INSPECTA_00-HLR-1) The firewall shall drop any frame that is malformed.
        final(api).EthernetFramesRxIn.is_some() ==>
          GumboLib::isMalformedFrame_spec(final(api).EthernetFramesRxIn.unwrap()) ==> final(api).EthernetFramesRxOut.is_none(),
        // guarantee RC_INSPECTA_00_HLR_4
        //   1.4 firewall: drop ipv6 frames (RC_INSPECTA_00-HLR-2) The firewall shall drop any frame that is type ipv6.
        final(api).EthernetFramesRxIn.is_some() ==>
          GumboLib::isIPV6_spec(final(api).EthernetFramesRxIn.unwrap()) ==> final(api).EthernetFramesRxOut.is_none(),
        // guarantee RC_INSPECTA_00_HLR_6
        //   1.6 firewall: drop RxIn ipv4 arp frames (RC_INSPECTA_00-HLR-4) The firewall shall drop any frame from RxIn that is an Ipv4 frame whose protocol is ARP.
        final(api).EthernetFramesRxIn.is_some() ==>
          GumboLib::isARP_spec(final(api).EthernetFramesRxIn.unwrap()) ==> final(api).EthernetFramesRxOut.is_none(),
        // guarantee RC_INSPECTA_00_HLR_8
        //   1.8 firewall: drop RxIn ipv4 tcp frames with unexpected ports (RC_INSPECTA_00-HLR-6) The firewall shall drop any frame from RxIn that is an Ipv4 frame whose protocol is TCP and whose port is not defined in the port whitelist.
        final(api).EthernetFramesRxIn.is_some() ==>
          ((GumboLib::isIPV4_spec(final(api).EthernetFramesRxIn.unwrap()) && GumboLib::isTCP_spec(final(api).EthernetFramesRxIn.unwrap())) &&
            !(GumboLib::isPortWhitelisted_spec(final(api).EthernetFramesRxIn.unwrap()))) ==>
            final(api).EthernetFramesRxOut.is_none(),
        // guarantee RC_INSPECTA_00_HLR_9
        //   1.9 firewall: copy through allowed tcp port packets (RC_INSPECTA_00-HLR-8; revised CR-01: applies in Normal mode only) In Normal mode, the firewall shall copy any frame from RxIn that is a non-malformed Ipv4 frame with the TCP protocol and whose port is defined in the port whitelist to RxOut.
        final(api).EthernetFramesRxIn.is_some() ==>
          (((((final(api).CurrentMode == SW::Mode::Normal) &&
            GumboLib::isIPV4_spec(final(api).EthernetFramesRxIn.unwrap())) &&
            GumboLib::isTCP_spec(final(api).EthernetFramesRxIn.unwrap())) &&
            GumboLib::isPortWhitelisted_spec(final(api).EthernetFramesRxIn.unwrap())) &&
            !(GumboLib::isMalformedFrame_spec(final(api).EthernetFramesRxIn.unwrap()))) ==>
            final(api).EthernetFramesRxOut.is_some() &&
              (final(api).EthernetFramesRxIn.unwrap() == final(api).EthernetFramesRxOut.unwrap()),
        // guarantee CR01_Rx_ModeGate
        //   FirewallRx_Req_ModeGate (CR-01): in Init and RTL modes, drop every frame — no output regardless of input.
        !(final(api).CurrentMode == SW::Mode::Normal) ==> final(api).EthernetFramesRxOut.is_none(),
        // guarantee CR01_Rx_Count
        //   FirewallRx_Req_Count (CR-01): cumulative malformed-frame count since initialization, incremented on each malformed received frame, saturating at 6; mode-independent.
        ((final(api).EthernetFramesRxIn.is_some() && GumboLib::isMalformedFrame_spec(final(api).EthernetFramesRxIn.unwrap()) &&
          (old(self).malformedCount < 6i32) ==>
          (final(self).malformedCount == old(self).malformedCount + 1i32)) &&
          (final(api).EthernetFramesRxIn.is_some() && GumboLib::isMalformedFrame_spec(final(api).EthernetFramesRxIn.unwrap()) &&
            (old(self).malformedCount >= 6i32) ==>
            (final(self).malformedCount == old(self).malformedCount))) &&
          (!(final(api).EthernetFramesRxIn.is_some()) || !(GumboLib::isMalformedFrame_spec(final(api).EthernetFramesRxIn.unwrap())) ==>
            (final(self).malformedCount == old(self).malformedCount)),
        // guarantee CR01_Rx_Detect
        //   FirewallRx_Req_Detect (CR-01): report Attack when the (post-update) malformed count exceeds five, OK otherwise.
        ((final(self).malformedCount > 5i32) ==>
          (final(api).AttackStatusRx == SW::AttackStatus::Attack)) &&
          ((final(self).malformedCount <= 5i32) ==>
            (final(api).AttackStatusRx == SW::AttackStatus::OK)),
        // END MARKER TIME TRIGGERED ENSURES
    {
      log_info("compute entrypoint invoked");

      let mode = api.get_CurrentMode();
      let input = api.get_EthernetFramesRxIn();

      // CR-01 FirewallRx_Req_Count: mode-independent malformed-frame
      // counting, saturating at 6.
      if let Some(msg) = input {
        if msg.malformedFrame {
          if self.malformedCount < 6 {
            self.malformedCount = self.malformedCount + 1;
          }
        }
      }

      // CR-01 FirewallRx_Req_Detect: report from the post-update count
      // (latched by construction: the count never decreases).
      if self.malformedCount > 5 {
        api.put_AttackStatusRx(SW::AttackStatus::Attack);
      } else {
        api.put_AttackStatusRx(SW::AttackStatus::OK);
      }

      // CR-01 FirewallRx_Req_ModeGate: frames flow only in Normal mode.
      // The Normal-mode branch is the unmodified baseline mediation logic.
      match mode {
        SW::Mode::Normal => {
          if let Some(msg) = input
          {
            match msg.internetProtocol
            {
              SW::InternetProtocol::IPV4 =>
              {
                match msg.frameProtocol
                {
                  SW::FrameProtocol::TCP =>
                  {
                    if msg.portIsWhitelisted == true
                    {
                      if msg.malformedFrame == false
                      {
                        api.put_EthernetFramesRxOut(msg);
                        log_message_passed(msg);
                      }
                    }
                    else
                    {
                      log_message_dropped(msg);
                    }
                  },
                  SW::FrameProtocol::ARP =>
                  {
                    log_message_dropped(msg);
                  }
                }
              },
              SW::InternetProtocol::IPV6 =>
              {
                log_message_dropped(msg);
              }
            }
          }
        },
        _ => {
          if let Some(msg) = input {
            log_message_dropped_mode(msg);
          }
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

    // Logging method for dropped messages.
  #[verifier::external_body]
  pub fn log_message_dropped(msg: SW::StructuredEthernetMessage_i)
  {
    log::info!("Rx Firewall: DROPPED message (internetProtocol={0:?})",
      msg.internetProtocol);
  }

  // Logging method for passed messages.
  #[verifier::external_body]
  pub fn log_message_passed(msg: SW::StructuredEthernetMessage_i)
  {
    log::info!("Rx Firewall: PASSED message (internetProtocol={0:?})",
      msg.internetProtocol);
  }

  // CR-01: logging method for frames dropped by the mode gate (Init/RTL).
  #[verifier::external_body]
  pub fn log_message_dropped_mode(msg: SW::StructuredEthernetMessage_i)
  {
    log::info!("Rx Firewall: DROPPED message - non-Normal mode (internetProtocol={0:?})",
      msg.internetProtocol);
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
