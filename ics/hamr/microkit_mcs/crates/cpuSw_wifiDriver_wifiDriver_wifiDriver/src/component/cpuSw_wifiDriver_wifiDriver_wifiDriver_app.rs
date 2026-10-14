// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::cpuSw_wifiDriver_wifiDriver_wifiDriver_api::*;
use vstd::prelude::*;

verus! {

  pub struct cpuSw_wifiDriver_wifiDriver_wifiDriver {
    // BEGIN MARKER STATE VARS
    pub alert_cmd: bool,
    // END MARKER STATE VARS
  }

  impl cpuSw_wifiDriver_wifiDriver_wifiDriver {
    pub fn new() -> Self
    {
      Self {
        // BEGIN MARKER STATE VAR INIT
        alert_cmd: false,
        // END MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: cpuSw_wifiDriver_wifiDriver_wifiDriver_Put_Api> (
      &mut self,
      api: &mut cpuSw_wifiDriver_wifiDriver_wifiDriver_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee defaultAlert
        final(self).alert_cmd == false,
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: cpuSw_wifiDriver_wifiDriver_wifiDriver_Full_Api> (
      &mut self,
      api: &mut cpuSw_wifiDriver_wifiDriver_wifiDriver_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).wifiSend.is_none(),
        old(api).HMD_log.is_none(),
        old(api).analysis_request.is_none(),
        // assume IncomingAlert
        //   A: A report should not be received if an alert is received.
        old(api).alert_in.is_some() ==> !(old(api).analysis_report.is_some()),
        // assume Trusted_Report
        //   A: Reports received are to a trusted destination.
        old(api).analysis_report.is_some() ==> MATRICS_Model_Transformations::FOUND_IN_ALLOW_LIST_spec(old(api).analysis_report.unwrap().header.client),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee alert_cmd_variable
        //   G: Once an alert command is seen, always stay alerted.
        final(self).alert_cmd == (final(api).alert_in.is_some() || old(self).alert_cmd),
        // guarantee Process_Report
        //   G: Stop outgoing communication once an alert has been received.
        if (final(api).analysis_report.is_some() && !final(self).alert_cmd) {
          final(api).wifiSend.is_some() &&
            (final(api).wifiSend.unwrap() == final(api).analysis_report.unwrap())
        } else {
          final(api).wifiSend.is_none()
        },
        // END MARKER TIME TRIGGERED ENSURES
    {
      let wifi_rx_message = api.get_wifiRecv();
      if wifi_rx_message.is_some() {
          let len = wifi_rx_message.unwrap().header.route.iter().position(|&b| b == 0).unwrap_or(0); // Find null byte
          let start = wifi_rx_message.unwrap().header.route.iter().position(|&b| b == b'/').unwrap_or(0); // Find first character
          if len > 0 && start > 0 {
               match core::str::from_utf8(&wifi_rx_message.unwrap().header.route[start..len]) {
                    Ok(v) => {
                         if v == "/hmd"{
                              api.put_HMD_log(wifi_rx_message.unwrap().payload);
                         }
                    },
                    Err(e) => panic!("Invalid UTF-8: {}", e),
               };
          }
      }
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
