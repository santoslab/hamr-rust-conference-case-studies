// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_api::*;
use vstd::prelude::*;

verus! {

  pub struct actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_Put_Api> (
      &mut self,
      api: &mut actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");

      // The Initialize Entry Point must initialize all component local state and all output data ports.
      // -- initialize output data port
      api.put_actuate(false);
    }

    pub fn timeTriggered<API: actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_Full_Api> (
      &mut self,
      api: &mut actuationSubsystem_actuationUnit2_temperatureLogic_coincidenceLogic_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee coincidenceOutput
        //   from actuationUnit.cry
        //   Coincidence_2_4 : [4]TripPort -> Bit
        //   Coincidence_2_4 x =
        //       (a&&b) || ((a||b) && (c||d)) || (c&&d)
        //   For specification redundancy, provide an alternate but equivalent specification
        //   of the concept 'at least two of the input channels are true.'
        final(api).actuate == ((((((final(api).channel1 && final(api).channel2) ||
          (final(api).channel1 && final(api).channel3)) ||
          (final(api).channel1 && final(api).channel4)) ||
          (final(api).channel2 && final(api).channel3)) ||
          (final(api).channel2 && final(api).channel4)) ||
          (final(api).channel3 && final(api).channel4)),
        // END MARKER TIME TRIGGERED ENSURES
    {
      // get values off of input ports.
      let a: bool = api.get_channel1();
      let b: bool = api.get_channel2();
      let c: bool = api.get_channel3();
      let d: bool = api.get_channel4();

      // from actuationUnit.cry
      //   Coincidence_2_4 : [4]TripPort -> Bit
      //   Coincidence_2_4 x =
      //     (a&&b) || ((a||b) && (c||d)) || (c&&d)
      //
      // Transliterate the Cryptol coincidence expression into Rust. (The Slang
      // version uses the non-short-circuit operators & and |; Verus does not
      // support those on bool, and with side-effect-free operands && and ||
      // compute the same result.)
      let result: bool = (a && b) || ((a || b) && (c || d)) || (c && d);

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
