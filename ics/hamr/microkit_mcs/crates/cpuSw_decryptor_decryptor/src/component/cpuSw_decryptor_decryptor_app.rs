// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use crate::bridge::cpuSw_decryptor_decryptor_api::*;
use vstd::prelude::*;
use base64::{Engine as _, engine::general_purpose};
use aes_gcm::{
     aead::{AeadCore, AeadInPlace, consts::{U12,U16}},
     Aes128Gcm, Nonce, Key, KeyInit, Tag
};

verus! {

  pub struct cpuSw_decryptor_decryptor {
    // PLACEHOLDER MARKER STATE VARS
    pub cipher: Aes128Gcm,
  }

  impl cpuSw_decryptor_decryptor {
    pub fn new() -> Self
    {
     let key = Key::<Aes128Gcm>::from_slice(b"\xa8\xf0\xe5\x78\xe8\x26\x08\x6d\x30\x42\xa0\x50\x22\xa7\x8b\x26"); // Shared key between client and server
      Self {
        // PLACEHOLDER MARKER STATE VAR INIT
        cipher: Aes128Gcm::new(key),
      }
    }

    pub fn initialize<API: cpuSw_decryptor_decryptor_Put_Api> (
      &mut self,
      api: &mut cpuSw_decryptor_decryptor_Application_Api<API>)
      ensures
        // PLACEHOLDER MARKER INITIALIZATION ENSURES
    {
      // log_info("initialize entrypoint invoked");
    }

    pub fn timeTriggered<API: cpuSw_decryptor_decryptor_Full_Api> (
      &mut self,
      api: &mut cpuSw_decryptor_decryptor_Application_Api<API>)
      requires
        // BEGIN MARKER TIME TRIGGERED REQUIRES
        // assume AADL_Requirement
        //   All outgoing event ports must be empty
        old(api).HMD_log_out.is_none(),
        // END MARKER TIME TRIGGERED REQUIRES
      ensures
        // BEGIN MARKER TIME TRIGGERED ENSURES
        // guarantee Payload_Decrypted
        //   G: Outgoing payload is decrypted.
        final(api).HMD_log_in.is_some() ==> MATRICS_Model_Transformations::AES_128_GCM_DECRYPTS_LOG_spec(final(api).HMD_log_in.unwrap(), final(api).HMD_log_out.unwrap()),
        // END MARKER TIME TRIGGERED ENSURES
    {
          let Some(mut encrypted) = api.get_HMD_log_in() else {
               return;
          };

          log::info!("Nonce: {:?}", encrypted.nonce);
          log::info!("Ciphertext: {:?}", encrypted.ciphertext);
          log::info!("Tag: {:?}", encrypted.tag);
          let nonce = Nonce::<U12>::from_slice(&encrypted.nonce);
          let tag = Tag::<U16>::from_slice(&encrypted.tag);
          match self.cipher.decrypt_in_place_detached(&nonce, b"", &mut encrypted.ciphertext, &tag) {
               Ok(()) => {
                    // Success: 'cyphertext' now contains the valid plaintext
                    match core::str::from_utf8(&encrypted.ciphertext) {
                         Ok(v) => {
                              log::info!("Decrypted Payload: {}", v);
                         },
                         Err(e) => panic!("Invalid UTF-8: {}", e),
                    };
               }
               Err(e) => {
                    // Failure: Data is corrupted or tag is wrong. 
                    // DO NOT trust the 'buffer' contents.
                    log::info!("Authentication failed: {}", e);
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
