// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_api::*;
use vstd::prelude::*;

verus! {

  pub struct actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_Put_Api> (
      &mut self,
      api: &mut actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee initOutputDataPort
        //   The Initialize Entry Point must initialize all component
        //   local state and all output data ports.
        final(api).output == false,
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");

      // The Initialize Entry Point must initialize all component local state and all output data ports.
      // -- initialize output data port
      api.put_output(false);
    }

    pub fn timeTriggered<API: actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_Full_Api> (
      &mut self,
      api: &mut actuationSubsystem_tempPressureActuatorUnit_tempPressureActuator_actuator_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee actuatorOutput
        final(api).output == (final(api).input || final(api).manualActuatorInput),
        // END MARKER TIME TRIGGERED ENSURES
    {
      // get values off of input ports.
      let input: bool = api.get_input();
      let manual_input: bool = api.get_manualActuatorInput();

      let output: bool = input || manual_input;

      // put calculated value on output data port
      api.put_output(output);
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
