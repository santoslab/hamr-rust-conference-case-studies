// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::cpuSw_logMonitor_logMonitor_api::*;
use vstd::prelude::*;

verus! {

  pub struct cpuSw_logMonitor_logMonitor {
    // BEGIN MARKER STATE VARS
    pub since_result: bool,
    pub is_valid: bool,
    pub historically_no_alert_cmd: bool,
    // END MARKER STATE VARS
  }

  impl cpuSw_logMonitor_logMonitor {
    pub fn new() -> Self
    {
      Self {
        // BEGIN MARKER STATE VAR INIT
        since_result: false,
        is_valid: false,
        historically_no_alert_cmd: false,
        // END MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: cpuSw_logMonitor_logMonitor_Put_Api> (
      &mut self,
      api: &mut cpuSw_logMonitor_logMonitor_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee defaultSince
        final(self).since_result == false,
        // guarantee defaultHistorically
        final(self).historically_no_alert_cmd == true,
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: cpuSw_logMonitor_logMonitor_Full_Api> (
      &mut self,
      api: &mut cpuSw_logMonitor_logMonitor_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).response_log_out.is_none(),
        old(api).alert_out.is_none(),
        old(api).storage_alert_out.is_none(),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee is_valid_variable
        //   G: is_valid set correctly
        final(self).is_valid ==
          (if (final(api).request_log.is_some() && final(api).response_log_in.is_some()) {
            true
          } else {
            final(api).response_log_in.is_some() ==> old(self).since_result
          }),
        // guarantee since_result_variable
        //   G: since_result is equivalent to (not response_log_in event) Since (request_log event)
        final(self).since_result == GUMBO_PLTL::AGREE_Since_spec(!(final(api).response_log_in.is_some()), final(api).request_log.is_some(), old(self).since_result),
        // guarantee historically_no_alert_cmd_variable
        //   G: historically_no_alert_cmd is true if and only if no alert has been sent.
        final(self).historically_no_alert_cmd == (old(self).historically_no_alert_cmd && !(final(api).alert_out.is_some())),
        // guarantee Send_Alert
        //   G: Send an alert if more than one response is received without a request.
        if (final(api).response_log_in.is_some() && !final(self).is_valid) {
          final(api).alert_out.is_some() && final(api).storage_alert_out.is_some()
        } else {
          final(api).alert_out.is_none() && final(api).storage_alert_out.is_none()
        },
        // guarantee Forward_Response
        //   G: Only forward a response if a valid request has been made.
        if (final(api).response_log_in.is_some() && final(self).historically_no_alert_cmd) {
          final(api).response_log_out.is_some() &&
            (final(api).response_log_out.unwrap() == final(api).response_log_in.unwrap())
        } else {
          final(api).response_log_out.is_none()
        },
        // END MARKER TIME TRIGGERED ENSURES
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
