// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::LowLevelEthernetDriver_LowLevelEthernetDriver_api::*;
use vstd::prelude::*;

verus! {

  pub struct LowLevelEthernetDriver_LowLevelEthernetDriver {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl LowLevelEthernetDriver_LowLevelEthernetDriver {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: LowLevelEthernetDriver_LowLevelEthernetDriver_Put_Api> (
      &mut self,
      api: &mut LowLevelEthernetDriver_LowLevelEthernetDriver_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: LowLevelEthernetDriver_LowLevelEthernetDriver_Full_Api> (
      &mut self,
      api: &mut LowLevelEthernetDriver_LowLevelEthernetDriver_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // PLACEHOLDER MARKER TIME TRIGGERED ENSURES
    {
      log_info("compute entrypoint invoked");
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
