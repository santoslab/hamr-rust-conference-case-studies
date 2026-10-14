// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::cpuSw_dataManager_dataManager_dataManager_api::*;
use vstd::prelude::*;

verus! {

  pub struct cpuSw_dataManager_dataManager_dataManager {
    // BEGIN MARKER STATE VARS
    pub zeroize_cmd: bool,
    // END MARKER STATE VARS
  }

  impl cpuSw_dataManager_dataManager_dataManager {
    pub fn new() -> Self
    {
      Self {
        // BEGIN MARKER STATE VAR INIT
        zeroize_cmd: false,
        // END MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: cpuSw_dataManager_dataManager_dataManager_Put_Api> (
      &mut self,
      api: &mut cpuSw_dataManager_dataManager_dataManager_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee defaultZeroize
        final(self).zeroize_cmd == false,
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: cpuSw_dataManager_dataManager_dataManager_Full_Api> (
      &mut self,
      api: &mut cpuSw_dataManager_dataManager_dataManager_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).encrypted_log.is_none(),
        old(api).storage_request.is_none(),
        old(api).response_log.is_none(),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee zeroize_cmd_variable
        //   G: Once a zeroize command is seen, always zeroize.
        final(self).zeroize_cmd == (final(api).zeroize.is_some() || old(self).zeroize_cmd),
        // guarantee Zeroize_Payload
        //   G: Zeroize outgoing responses once an alert is received and when a request has been made.
        (final(self).zeroize_cmd && final(api).request_log.is_some()) ==>
          IS_ZEROIZED(final(api).response_log.unwrap().payload),
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
  pub open spec fn IS_ZEROIZED(response: Common::Response_Impl) -> bool
  {
    (((MATRICS_Model_Transformations::IS_NULL_REQUEST_spec(response.request) &&
      (response.validLogCount == 0u32)) &&
      (response.moreAvailable == false)) &&
      (response.nextStartTime == 0u64)) &&
      #[trigger] forall|response_log_index:int| 0 <= response_log_index <= response.logs.len() - 1 ==> MATRICS_Model_Transformations::IS_NULL_LOG_spec(response.logs[response_log_index])
  }
  // END MARKER GUMBO METHODS

}
