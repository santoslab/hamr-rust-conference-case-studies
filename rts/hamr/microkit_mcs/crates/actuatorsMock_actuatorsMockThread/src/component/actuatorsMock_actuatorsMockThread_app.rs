// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::actuatorsMock_actuatorsMockThread_api::*;
use vstd::prelude::*;

verus! {

  pub struct actuatorsMock_actuatorsMockThread {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl actuatorsMock_actuatorsMockThread {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: actuatorsMock_actuatorsMockThread_Put_Api> (
      &mut self,
      api: &mut actuatorsMock_actuatorsMockThread_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: actuatorsMock_actuatorsMockThread_Full_Api> (
      &mut self,
      api: &mut actuatorsMock_actuatorsMockThread_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // PLACEHOLDER MARKER TIME TRIGGERED ENSURES
    {
      let temp_pressure: bool = api.get_tempPressureActuate();
      let saturation: bool = api.get_saturationActuate();
      log_actuation(temp_pressure, saturation);
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

  #[verifier::external_body]
  pub fn log_actuation(temp_pressure: bool, saturation: bool)
  {
    log::info!("Received on tempPressureActuate: {0}", temp_pressure);
    log::info!("Received on saturationActuate: {0}", saturation);
  }

  // PLACEHOLDER MARKER GUMBO METHODS

}
