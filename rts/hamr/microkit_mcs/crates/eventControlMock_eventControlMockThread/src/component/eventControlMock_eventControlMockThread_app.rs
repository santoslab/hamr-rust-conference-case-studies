// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::eventControlMock_eventControlMockThread_api::*;
use vstd::prelude::*;

verus! {

  pub struct eventControlMock_eventControlMockThread {
    // PLACEHOLDER MARKER STATE VARS
    pub frame: usize,
  }

  impl eventControlMock_eventControlMockThread {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
        frame: 0,
      }
    }

    pub fn initialize<API: eventControlMock_eventControlMockThread_Put_Api> (
      &mut self,
      api: &mut eventControlMock_eventControlMockThread_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("Initialize Entry Point: Event Control Mock");

      // AADL computational model requires that we provide an initial value on output data ports
      api.put_manualActuatorInput1(false);
      api.put_manualActuatorInput2(false);
    }

    pub fn timeTriggered<API: eventControlMock_eventControlMockThread_Full_Api> (
      &mut self,
      api: &mut eventControlMock_eventControlMockThread_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // PLACEHOLDER MARKER TIME TRIGGERED ENSURES
    {
      let frame: usize = if self.frame < NUM_FRAMES { self.frame } else { 0 };
      let inputs = FRAMES[frame];
      log_frame(frame, &inputs);
      api.put_manualActuatorInput1(inputs[0]);
      api.put_manualActuatorInput2(inputs[1]);

      // Move to the next frame
      self.frame = if frame + 1 == NUM_FRAMES { 0 } else { frame + 1 };
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

  // Mocked event control behavior is to send out the following manual trip signals
  // (manualActuatorInput1, manualActuatorInput2), one pair per dispatch (then repeat).
  pub const NUM_FRAMES: usize = 9;

  pub const FRAMES: [[bool; 2]; NUM_FRAMES] = [
    [false, false],
    [false, false],
    [false, false],
    [false, false],
    [false, false],
    [false, false],
    [true, false],
    [true, true],
    [false, false],
  ];

  #[verifier::external_body]
  pub fn log_frame(frame: usize, inputs: &[bool; 2])
  {
    log::info!("Event Control: Frame: {0}", frame);
    log::info!("  Event Control test vector: {0:?}", inputs);
  }

  // PLACEHOLDER MARKER GUMBO METHODS

}
