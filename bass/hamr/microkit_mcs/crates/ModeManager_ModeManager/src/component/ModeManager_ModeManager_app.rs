// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::ModeManager_ModeManager_api::*;
use vstd::prelude::*;

verus! {

  pub struct ModeManager_ModeManager {
    // BEGIN MARKER STATE VARS
    pub currentMode: SW::Mode,
    pub activationCount: i32,
    // END MARKER STATE VARS
  }

  impl ModeManager_ModeManager {
    pub fn new() -> Self
    {
      Self {
        // BEGIN MARKER STATE VAR INIT
        currentMode: SW::Mode::default(),
        activationCount: 0,
        // END MARKER STATE VAR INIT
      }
    }

    pub fn initialize<API: ModeManager_ModeManager_Put_Api> (
      &mut self,
      api: &mut ModeManager_ModeManager_Application_Api<API>)
      ensures
        // BEGIN MARKER INITIALIZATION ENSURES
        // guarantee CR01_MM_Init
        //   ModeManager_Req_Init: start in Init with zero activations; mode DataPort initialized to Init.
        ((final(self).currentMode == SW::Mode::Init) &&
          (final(self).activationCount == 0i32)) &&
          (final(api).CurrentMode == SW::Mode::Init),
        // END MARKER INITIALIZATION ENSURES
    {
      log_info("initialize entrypoint invoked");

      // ModeManager_Req_Init: start in Init with zero activations; the mode
      // DataPort must be initialized (its value is sampled by the firewalls
      // before any first compute dispatch).
      self.currentMode = SW::Mode::Init;
      self.activationCount = 0;
      api.put_CurrentMode(SW::Mode::Init);
    }

    pub fn timeTriggered<API: ModeManager_ModeManager_Full_Api> (
      &mut self,
      api: &mut ModeManager_ModeManager_Application_Api<API>)
      requires
        // PLACEHOLDER MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee CR01_MM_Count
        //   ModeManager_Req_Count: activation counter increments each dispatch, saturating at 10.
        ((old(self).activationCount < 10i32) ==>
          (final(self).activationCount == old(self).activationCount + 1i32)) &&
          ((old(self).activationCount >= 10i32) ==>
            (final(self).activationCount == old(self).activationCount)),
        // guarantee CR01_MM_Absorbing
        //   ModeManager_Req_Absorbing: RTL is absorbing until restart (RD-3).
        (old(self).currentMode == SW::Mode::RTL) ==>
          (final(self).currentMode == SW::Mode::RTL),
        // guarantee CR01_MM_ToRTL
        //   ModeManager_Req_ToRTL: when not already in RTL and either firewall reports Attack, enter RTL (wins ties against Init-to-Normal).
        (!(old(self).currentMode == SW::Mode::RTL) &&
          (GumboLib::isAttack_spec(final(api).AttackStatusRx) || GumboLib::isAttack_spec(final(api).AttackStatusTx))) ==>
          (final(self).currentMode == SW::Mode::RTL),
        // guarantee CR01_MM_StayInit
        //   ModeManager_Req_StayInit: in Init with no attack and (post-increment) count below 10, remain in Init.
        (((old(self).currentMode == SW::Mode::Init) &&
          !(GumboLib::isAttack_spec(final(api).AttackStatusRx) || GumboLib::isAttack_spec(final(api).AttackStatusTx))) &&
          (final(self).activationCount < 10i32)) ==>
          (final(self).currentMode == SW::Mode::Init),
        // guarantee CR01_MM_ToNormal
        //   ModeManager_Req_ToNormal: in Init with no attack and (post-increment) count reaching 10, transition to Normal.
        (((old(self).currentMode == SW::Mode::Init) &&
          !(GumboLib::isAttack_spec(final(api).AttackStatusRx) || GumboLib::isAttack_spec(final(api).AttackStatusTx))) &&
          (final(self).activationCount >= 10i32)) ==>
          (final(self).currentMode == SW::Mode::Normal),
        // guarantee CR01_MM_StayNormal
        //   ModeManager_Req_StayNormal: in Normal with no attack, remain in Normal.
        ((old(self).currentMode == SW::Mode::Normal) &&
          !(GumboLib::isAttack_spec(final(api).AttackStatusRx) || GumboLib::isAttack_spec(final(api).AttackStatusTx))) ==>
          (final(self).currentMode == SW::Mode::Normal),
        // guarantee CR01_MM_Broadcast
        //   ModeManager_Req_Broadcast: the mode DataPort output equals the post-transition mode state.
        final(api).CurrentMode == final(self).currentMode,
        // END MARKER TIME TRIGGERED ENSURES
    {
      log_info("compute entrypoint invoked");

      let rx_status = api.get_AttackStatusRx();
      let tx_status = api.get_AttackStatusTx();

      // ModeManager_Req_Count: activation counter, saturating at 10
      if self.activationCount < 10 {
        self.activationCount = self.activationCount + 1;
      }

      // Enum comparison via match (Verus cannot use the derived == here)
      let attack: bool = match (rx_status, tx_status) {
        (SW::AttackStatus::OK, SW::AttackStatus::OK) => false,
        _ => true,
      };

      match self.currentMode {
        SW::Mode::RTL => {
          // ModeManager_Req_Absorbing: RTL until restart
        },
        SW::Mode::Init => {
          if attack {
            // ModeManager_Req_ToRTL (wins ties against Init-to-Normal)
            self.currentMode = SW::Mode::RTL;
            log_entered_rtl();
          } else if self.activationCount >= 10 {
            // ModeManager_Req_ToNormal: 10th activation
            self.currentMode = SW::Mode::Normal;
            log_entered_normal();
          }
          // else ModeManager_Req_StayInit
        },
        SW::Mode::Normal => {
          if attack {
            // ModeManager_Req_ToRTL
            self.currentMode = SW::Mode::RTL;
            log_entered_rtl();
          }
          // else ModeManager_Req_StayNormal
        },
      }

      // ModeManager_Req_Broadcast: output mirrors the post-transition mode
      api.put_CurrentMode(self.currentMode);
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

  #[verifier::external_body]
  pub fn log_entered_normal()
  {
    log::info!("ModeManager: entered Normal mode (10th activation)");
  }

  #[verifier::external_body]
  pub fn log_entered_rtl()
  {
    log::info!("ModeManager: attack reported - entered RTL mode (absorbing)");
  }

  // PLACEHOLDER MARKER GUMBO METHODS

}
