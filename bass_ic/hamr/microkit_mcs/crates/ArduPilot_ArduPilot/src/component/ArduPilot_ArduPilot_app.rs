// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::ArduPilot_ArduPilot_api::*;
use vstd::prelude::*;

verus! {

  pub struct ArduPilot_ArduPilot {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl ArduPilot_ArduPilot {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: ArduPilot_ArduPilot_Put_Api> (
      &mut self,
      api: &mut ArduPilot_ArduPilot_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: ArduPilot_ArduPilot_Full_Api> (
      &mut self,
      api: &mut ArduPilot_ArduPilot_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // PLACEHOLDER MARKER TIME TRIGGERED ENSURES
    {
      // Stand-in for ArduPilot's network stack: answer each frame received from
      // the RxFirewall by sending it back out through the TxFirewall.
      //
      // put_EthernetFramesTx requires TxOut_IPv4OrARP (the frame is IPv4 or ARP).
      // That follows from RxIn_NoBlockedFrames, which get_EthernetFramesRx ensures:
      // a received frame is not one the RxFirewall must drop, so it is not IPv6.
      if let Some(frame) = api.get_EthernetFramesRx() {
        api.put_EthernetFramesTx(frame);
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

  // PLACEHOLDER MARKER GUMBO METHODS

}
