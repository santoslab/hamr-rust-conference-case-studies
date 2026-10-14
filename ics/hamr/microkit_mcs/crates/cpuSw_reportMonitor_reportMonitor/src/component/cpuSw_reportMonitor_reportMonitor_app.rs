// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::cpuSw_reportMonitor_reportMonitor_api::*;
use vstd::prelude::*;

verus! {

  pub struct cpuSw_reportMonitor_reportMonitor {
    // BEGIN MARKER STATE VARS
    pub counter: u32,
    pub since_result: bool,
    pub is_valid1: bool,
    pub is_invalid2: bool,
    // END MARKER STATE VARS
  }

  impl cpuSw_reportMonitor_reportMonitor {
    pub fn new() -> Self
    {
      Self {
        // BEGIN MARKER STATE VAR INIT
        counter: 0,
        since_result: false,
        is_valid1: false,
        is_invalid2: false,
        // END MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: cpuSw_reportMonitor_reportMonitor_Put_Api> (
      &mut self,
      api: &mut cpuSw_reportMonitor_reportMonitor_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee defaultCounterAndSince
        (final(self).counter == 0u32) &&
          (final(self).since_result == false),
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: cpuSw_reportMonitor_reportMonitor_Full_Api> (
      &mut self,
      api: &mut cpuSw_reportMonitor_reportMonitor_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).analysis_report_out.is_none(),
        old(api).alert_out.is_none(),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee counter_variable
        //   G: counter set correctly
        final(self).counter == Counter(final(api).analysis_request.is_some(), final(api).analysis_report_in.is_some(), old(self).counter),
        // guarantee since_result_variable
        //   G: Internal variable since_result is equivalent to (not analysis_report_in event) Since (analysis_request event)
        final(self).since_result == GUMBO_PLTL::AGREE_Since_spec(!(final(api).analysis_report_in.is_some()), final(api).analysis_request.is_some(), old(self).since_result),
        // guarantee valid1
        //   G: is_valid1 set correctly
        if (final(api).analysis_report_in.is_some() && final(api).analysis_request.is_some()) {
          final(self).is_valid1 == true
        } else {
          final(self).is_valid1 == (final(api).analysis_report_in.is_some() ==> old(self).since_result)
        },
        // guarantee invalid2
        //   G: is_invalid2 set correctly
        final(self).is_invalid2 == (final(self).counter >= 3u32),
        // guarantee Send_Alert
        //   G: Send an alert if a report is received without a valid request or if three or more requests are received without a report.
        if ((final(api).analysis_report_in.is_some() && !final(self).is_valid1) ||
          final(self).is_invalid2) {
          final(api).alert_out.is_some()
        } else {
          final(api).alert_out.is_none()
        },
        // guarantee Forward_Report
        //   G: Only forward a report if a valid request has been made and it is to a trusted destination.
        if (((final(api).analysis_report_in.is_some() && final(self).is_valid1) &&
          !final(self).is_invalid2) &&
          MATRICS_Model_Transformations::FOUND_IN_ALLOW_LIST_spec(final(api).analysis_report_in.unwrap().header.client)) {
          final(api).analysis_report_out.is_some() &&
            (final(api).analysis_report_out.unwrap() == final(api).analysis_report_in.unwrap())
        } else {
          final(api).analysis_report_out.is_none()
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

  // BEGIN MARKER GUMBO METHODS
  pub open spec fn Counter(
    i: bool,
    reset: bool,
    count: u32) -> u32
  {
    if (reset) {
      0u32
    } else {
      if (i) {
        (count + 1u32) as u32
      } else {
        count
      }
    }
  }
  // END MARKER GUMBO METHODS

}
