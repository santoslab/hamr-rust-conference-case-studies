// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::cpuSw_encryptor_encryptor_api::*;
use vstd::prelude::*;

verus! {

  pub struct cpuSw_encryptor_encryptor {
    // PLACEHOLDER MARKER STATE VARS
  }

  impl cpuSw_encryptor_encryptor {
    pub fn new() -> Self
    {
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: cpuSw_encryptor_encryptor_Put_Api> (
      &mut self,
      api: &mut cpuSw_encryptor_encryptor_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: cpuSw_encryptor_encryptor_Full_Api> (
      &mut self,
      api: &mut cpuSw_encryptor_encryptor_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).analysis_report_out.is_none(),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee Payload_Encrypted
        //   G: Outgoing payload is encrypted.
        final(api).analysis_report_in.is_some() ==> MATRICS_Model_Transformations::AES_128_GCM_ENCRYPTS_RESPONSE_spec(final(api).analysis_report_in.unwrap().payload, final(api).analysis_report_out.unwrap().payload),
        // guarantee Header_Unencrypted
        //   G: Outgoing header is not encrypted.
        final(api).analysis_report_out.unwrap().header == final(api).analysis_report_in.unwrap().header,
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
