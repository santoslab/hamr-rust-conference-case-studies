// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::instrumentationMock_instrumentationMockThread_api::*;
use vstd::prelude::*;

verus! {

  pub struct instrumentationMock_instrumentationMockThread {
    // PLACEHOLDER MARKER STATE VARS
    pub frame: usize,
  }

  impl instrumentationMock_instrumentationMockThread {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
        frame: 0,
      }
    }

    pub fn initialize<API: instrumentationMock_instrumentationMockThread_Put_Api> (
      &mut self,
      api: &mut instrumentationMock_instrumentationMockThread_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");

      // AADL computational model requires that we provide an initial value on output data ports
      api.put_unit1_temperatureLogic_channel1(false);
      api.put_unit1_temperatureLogic_channel2(false);
      api.put_unit1_temperatureLogic_channel3(false);
      api.put_unit1_temperatureLogic_channel4(false);
      api.put_unit1_pressureLogic_channel1(false);
      api.put_unit1_pressureLogic_channel2(false);
      api.put_unit1_pressureLogic_channel3(false);
      api.put_unit1_pressureLogic_channel4(false);
      api.put_unit1_saturationLogic_channel1(false);
      api.put_unit1_saturationLogic_channel2(false);
      api.put_unit1_saturationLogic_channel3(false);
      api.put_unit1_saturationLogic_channel4(false);
      api.put_unit2_temperatureLogic_channel1(false);
      api.put_unit2_temperatureLogic_channel2(false);
      api.put_unit2_temperatureLogic_channel3(false);
      api.put_unit2_temperatureLogic_channel4(false);
      api.put_unit2_pressureLogic_channel1(false);
      api.put_unit2_pressureLogic_channel2(false);
      api.put_unit2_pressureLogic_channel3(false);
      api.put_unit2_pressureLogic_channel4(false);
      api.put_unit2_saturationLogic_channel1(false);
      api.put_unit2_saturationLogic_channel2(false);
      api.put_unit2_saturationLogic_channel3(false);
      api.put_unit2_saturationLogic_channel4(false);
    }

    pub fn timeTriggered<API: instrumentationMock_instrumentationMockThread_Full_Api> (
      &mut self,
      api: &mut instrumentationMock_instrumentationMockThread_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // PLACEHOLDER MARKER TIME TRIGGERED ENSURES
    {
      // We do this one frame at a time to allow the rest of the system to run
      // through the logic and actuation before moving to the next frame.
      let frame: usize = if self.frame < NUM_FRAMES { self.frame } else { 0 };
      let (unit1, unit2) = frame_vectors(frame);
      log_frame(frame, &unit1, &unit2);

      api.put_unit1_temperatureLogic_channel1(unit1[0]);
      api.put_unit1_temperatureLogic_channel2(unit1[1]);
      api.put_unit1_temperatureLogic_channel3(unit1[2]);
      api.put_unit1_temperatureLogic_channel4(unit1[3]);
      api.put_unit1_pressureLogic_channel1(unit1[4]);
      api.put_unit1_pressureLogic_channel2(unit1[5]);
      api.put_unit1_pressureLogic_channel3(unit1[6]);
      api.put_unit1_pressureLogic_channel4(unit1[7]);
      api.put_unit1_saturationLogic_channel1(unit1[8]);
      api.put_unit1_saturationLogic_channel2(unit1[9]);
      api.put_unit1_saturationLogic_channel3(unit1[10]);
      api.put_unit1_saturationLogic_channel4(unit1[11]);

      api.put_unit2_temperatureLogic_channel1(unit2[0]);
      api.put_unit2_temperatureLogic_channel2(unit2[1]);
      api.put_unit2_temperatureLogic_channel3(unit2[2]);
      api.put_unit2_temperatureLogic_channel4(unit2[3]);
      api.put_unit2_pressureLogic_channel1(unit2[4]);
      api.put_unit2_pressureLogic_channel2(unit2[5]);
      api.put_unit2_pressureLogic_channel3(unit2[6]);
      api.put_unit2_pressureLogic_channel4(unit2[7]);
      api.put_unit2_saturationLogic_channel1(unit2[8]);
      api.put_unit2_saturationLogic_channel2(unit2[9]);
      api.put_unit2_saturationLogic_channel3(unit2[10]);
      api.put_unit2_saturationLogic_channel4(unit2[11]);

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

  // Mocked instrumentation behavior is to send out the following sets of trip
  // signals, one set per dispatch (then repeat). Each row lists, for one actuation
  // unit, the temperature, pressure, and saturation logic channels 1-4.
  pub const NUM_FRAMES: usize = 9;

  pub const UNIT1_FRAMES: [[bool; 12]; NUM_FRAMES] = [
    [true, false, false, false, true, false, false, true, false, false, false, false],
    [false, true, true, false, false, true, false, true, false, true, false, false],
    [false, false, false, true, false, false, false, false, false, true, true, false],
    [false, false, true, true, false, false, true, false, true, false, false, true],
    [false, false, false, false, true, false, false, false, false, false, false, false],
    [false, false, false, false, true, false, false, false, false, false, false, false],
    [true, false, false, false, false, false, false, false, false, false, false, false],
    [false, false, false, false, true, false, false, true, false, false, true, false],
    [false, false, false, false, true, false, false, true, false, false, true, false],
  ];

  pub const UNIT2_FRAMES: [[bool; 12]; NUM_FRAMES] = [
    [false, false, true, false, false, false, false, false, false, false, false, true],
    [false, false, false, false, false, true, true, false, false, false, false, true],
    [false, false, false, true, false, false, false, false, false, false, false, false],
    [false, false, false, false, false, false, true, false, false, false, false, true],
    [false, false, true, false, false, true, true, false, false, false, false, false],
    [false, false, true, false, false, false, false, false, false, true, false, true],
    [false, false, false, false, false, false, false, false, true, false, false, false],
    [false, false, true, false, false, false, false, false, true, false, false, true],
    [false, false, true, false, false, false, false, false, true, false, false, true],
  ];

  // Test-vector table lookup for the mock; the table is test data, not
  // application logic, so it is kept out of verification.
  #[verifier::external_body]
  pub fn frame_vectors(frame: usize) -> ([bool; 12], [bool; 12])
  {
    (UNIT1_FRAMES[frame], UNIT2_FRAMES[frame])
  }

  #[verifier::external_body]
  pub fn log_frame(frame: usize, unit1: &[bool; 12], unit2: &[bool; 12])
  {
    log::info!("Instrumentation: Frame: {0}", frame);
    log::info!("  Unit1 test vector: {0:?}", unit1);
    log::info!("  Unit2 test vector: {0:?}", unit2);
  }

  // PLACEHOLDER MARKER GUMBO METHODS

}
