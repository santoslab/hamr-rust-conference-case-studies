// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::cpuSw_dataAnalysis_dataAnalysis_api::*;
use vstd::prelude::*;

verus! {

  pub struct cpuSw_dataAnalysis_dataAnalysis {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl cpuSw_dataAnalysis_dataAnalysis {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: cpuSw_dataAnalysis_dataAnalysis_Put_Api> (
      &mut self,
      api: &mut cpuSw_dataAnalysis_dataAnalysis_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: cpuSw_dataAnalysis_dataAnalysis_Full_Api> (
      &mut self,
      api: &mut cpuSw_dataAnalysis_dataAnalysis_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).request_log.is_none(),
        old(api).analysis_report.is_none(),
        // assume Trusted_Request
        //   A: Requests received are from a trusted source.
        old(api).analysis_request.is_some() ==> MATRICS_Model_Transformations::FOUND_IN_ALLOW_LIST_spec(old(api).analysis_request.unwrap().header.client),
        // END MARKER TIME TRIGGERED REQUIRES
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
