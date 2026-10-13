// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_api::*;
use vstd::prelude::*;

verus! {

  pub struct actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_Put_Api> (
      &mut self,
      api: &mut actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");

      // The Initialize Entry Point must initialize all component local state and all output data ports.
      // -- initialize output data port
      api.put_actuate(false);
    }

    pub fn timeTriggered<API: actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_Full_Api> (
      &mut self,
      api: &mut actuationSubsystem_tempPressureActuatorUnit_actuateTempPressureActuator_orLogic_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee orOutput
        final(api).actuate == (final(api).channel1 || final(api).channel2),
        // END MARKER TIME TRIGGERED ENSURES
    {
      // get values off of input ports.
      let channel1: bool = api.get_channel1();
      let channel2: bool = api.get_channel2();

      // from actuationUnit.cry (line 53)
      //   TempPressureTripOut ts = (ts @ (0:[1])) || (ts @ (1:[1]))
      let result: bool = channel1 || channel2;

      // put calculated value on output data port
      api.put_actuate(result);
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
