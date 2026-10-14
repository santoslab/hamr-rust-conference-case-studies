#![cfg_attr(not(test), no_std)]

#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]

#![allow(dead_code)]
#![allow(static_mut_refs)]
#![allow(unused_imports)]
#![allow(unused_macros)]
#![allow(unused_parens)]
#![allow(unused_unsafe)]
#![allow(unused_variables)]

// The two features below are required by the Verus build but go unused on a
// plain cargo build, and `verus_keep_ghost` is set by Verus rather than
// declared to cargo, so both lints fire only on the non-Verus path.
#![allow(unused_features)]
#![allow(unexpected_cfgs)]

#![feature(proc_macro_hygiene)]
#![cfg_attr(not(verus_keep_ghost), feature(stmt_expr_attributes))]

// This file will not be overwritten if HAMR codegen is rerun

use data::*;
use vstd::prelude::*;

macro_rules! implies {
  ($lhs: expr, $rhs: expr) => {
    !$lhs || $rhs
  };
}

macro_rules! impliesL {
  ($lhs: expr, $rhs: expr) => {
    !$lhs | $rhs
  };
}

// BEGIN MARKER GUMBO RUST MARKER
pub fn FOUND_IN_ALLOW_LIST(src: u32) -> bool
{
  (src == 3232235877u32) ||
    (src == 3232235878u32) ||
    (src == 3232235879u32) ||
    (src == 3232235880u32)
}

/// GUMBOX wrapper for the GUMBO spec function `test` that delegates to the developer-supplied GUMBOX
/// specification function that must have the following signature:
/// 
///   pub exec fn AES_128_GCM_DECRYPTS_LOG__developer_gumbox(
///         encrypted_message: Common::EncryptedMessage_Impl,
///         decrypted: Common::Log_Impl) -> (res: bool) { ... }
/// 
/// The semantics of the GUMBO spec function are entirely defined by the developer-supplied implementation.
pub fn AES_128_GCM_DECRYPTS_LOG(
  encrypted_message: Common::EncryptedMessage_Impl,
  decrypted: Common::Log_Impl) -> bool
{
  AES_128_GCM_DECRYPTS_LOG__developer_gumbox(encrypted_message, decrypted)
}

/// GUMBOX wrapper for the GUMBO spec function `test` that delegates to the developer-supplied GUMBOX
/// specification function that must have the following signature:
/// 
///   pub exec fn AES_128_GCM_ENCRYPTS_RESPONSE__developer_gumbox(
///         response: Common::Response_Impl,
///         encrypted: Common::EncryptedMessage_Impl) -> (res: bool) { ... }
/// 
/// The semantics of the GUMBO spec function are entirely defined by the developer-supplied implementation.
pub fn AES_128_GCM_ENCRYPTS_RESPONSE(
  response: Common::Response_Impl,
  encrypted: Common::EncryptedMessage_Impl) -> bool
{
  AES_128_GCM_ENCRYPTS_RESPONSE__developer_gumbox(response, encrypted)
}

pub fn IS_NULL_HMD_POSITION(position: Common::HMDPosition_Impl) -> bool
{
  (position.positionX == 0i32) &
    (position.positionY == 0i32) &
    (position.positionZ == 0i32) &
    (position.orientationX == 0i32) &
    (position.orientationY == 0i32) &
    (position.orientationZ == 0i32) &
    (position.orientationW == 0i32)
}

pub fn IS_NULL_TARGET(target: Common::TargetObservation_Impl) -> bool
{
  (target.targetID == 0u32) &
    (target.locationX == 0i32) &
    (target.locationY == 0i32) &
    (target.locationZ == 0i32) &
    (target.assessment == Common::TargetAssessment::Unreviewed)
}

pub fn IS_NULL_LOG(log: Common::Log_Impl) -> bool
{
  (log.timestamp == 0u64) &
    (log.guardID == 0u32) &
    (log.deviceID == 0u32) &
    IS_NULL_HMD_POSITION(log.hmdPosition) &
    (log.targetCount == 0u32) &
    (0..=log.targets.len() - 1).all(|target_index| IS_NULL_TARGET(log.targets[target_index]))
}

pub fn IS_NULL_REQUEST(request: Common::Request_Impl) -> bool
{
  (request.analysisType == Common::AnalysisType::All_Records) &
    (request.guardID == 0u32) &
    (request.startTime == 0u64) &
    (request.endTime == 0u64) &
    (request.targetID == 0u32)
}
// END MARKER GUMBO RUST MARKER

verus! {

  // BEGIN MARKER GUMBO VERUS MARKER
  pub open spec fn FOUND_IN_ALLOW_LIST_spec(src: u32) -> bool
  {
    (src == 3232235877u32) ||
      (src == 3232235878u32) ||
      (src == 3232235879u32) ||
      (src == 3232235880u32)
  }

  /// Verus wrapper for the GUMBO spec function `test` that delegates to the developer-supplied Verus
  /// specification function that must have the following signature:
  /// 
  ///   pub open spec fn AES_128_GCM_DECRYPTS_LOG__developer_verus(
  ///         encrypted_message: Common::EncryptedMessage_Impl,
  ///         decrypted: Common::Log_Impl) -> (res: bool) { ... }
  /// 
  /// The semantics of the GUMBO spec function are entirely defined by the developer-supplied implementation.
  pub open spec fn AES_128_GCM_DECRYPTS_LOG_spec(
    encrypted_message: Common::EncryptedMessage_Impl,
    decrypted: Common::Log_Impl) -> bool
  {
    AES_128_GCM_DECRYPTS_LOG__developer_verus(encrypted_message, decrypted)
  }

  /// Verus wrapper for the GUMBO spec function `test` that delegates to the developer-supplied Verus
  /// specification function that must have the following signature:
  /// 
  ///   pub open spec fn AES_128_GCM_ENCRYPTS_RESPONSE__developer_verus(
  ///         response: Common::Response_Impl,
  ///         encrypted: Common::EncryptedMessage_Impl) -> (res: bool) { ... }
  /// 
  /// The semantics of the GUMBO spec function are entirely defined by the developer-supplied implementation.
  pub open spec fn AES_128_GCM_ENCRYPTS_RESPONSE_spec(
    response: Common::Response_Impl,
    encrypted: Common::EncryptedMessage_Impl) -> bool
  {
    AES_128_GCM_ENCRYPTS_RESPONSE__developer_verus(response, encrypted)
  }

  pub open spec fn IS_NULL_HMD_POSITION_spec(position: Common::HMDPosition_Impl) -> bool
  {
    ((((((position.positionX == 0i32) &&
      (position.positionY == 0i32)) &&
      (position.positionZ == 0i32)) &&
      (position.orientationX == 0i32)) &&
      (position.orientationY == 0i32)) &&
      (position.orientationZ == 0i32)) &&
      (position.orientationW == 0i32)
  }

  pub open spec fn IS_NULL_TARGET_spec(target: Common::TargetObservation_Impl) -> bool
  {
    ((((target.targetID == 0u32) &&
      (target.locationX == 0i32)) &&
      (target.locationY == 0i32)) &&
      (target.locationZ == 0i32)) &&
      (target.assessment == Common::TargetAssessment::Unreviewed)
  }

  pub open spec fn IS_NULL_LOG_spec(log: Common::Log_Impl) -> bool
  {
    (((((log.timestamp == 0u64) &&
      (log.guardID == 0u32)) &&
      (log.deviceID == 0u32)) &&
      IS_NULL_HMD_POSITION_spec(log.hmdPosition)) &&
      (log.targetCount == 0u32)) &&
      #[trigger] forall|target_index:int| 0 <= target_index <= log.targets.len() - 1 ==> IS_NULL_TARGET_spec(log.targets[target_index])
  }

  pub open spec fn IS_NULL_REQUEST_spec(request: Common::Request_Impl) -> bool
  {
    ((((request.analysisType == Common::AnalysisType::All_Records) &&
      (request.guardID == 0u32)) &&
      (request.startTime == 0u64)) &&
      (request.endTime == 0u64)) &&
      (request.targetID == 0u32)
  }
  // END MARKER GUMBO VERUS MARKER

  /// Developer-supplied Verus realization of the GUMBO spec function `test`.
  /// 
  /// This function may be freely refined as long as it remains a pure Verus `spec fn`.
  pub open spec fn AES_128_GCM_DECRYPTS_LOG__developer_verus(
    encrypted_message: Common::EncryptedMessage_Impl,
    decrypted: Common::Log_Impl) -> (res: bool)
  {
    // This default implementation returns `true`, which is safe but weak:
    // * In `assume` contexts, returning `false` may allow Verus to prove `false`.
    // * To obtain meaningful guarantees, developers should strengthen this
    //   specification to reflect the intended semantics of the GUMBO spec function.
    true
  }

  /// Developer-supplied Verus realization of the GUMBO spec function `test`.
  /// 
  /// This function may be freely refined as long as it remains a pure Verus `spec fn`.
  pub open spec fn AES_128_GCM_ENCRYPTS_RESPONSE__developer_verus(
    response: Common::Response_Impl,
    encrypted: Common::EncryptedMessage_Impl) -> (res: bool)
  {
    // This default implementation returns `true`, which is safe but weak:
    // * In `assume` contexts, returning `false` may allow Verus to prove `false`.
    // * To obtain meaningful guarantees, developers should strengthen this
    //   specification to reflect the intended semantics of the GUMBO spec function.
    true
  }

  /// Developer-supplied GUMBOX realization of the GUMBO spec function `test`.
  /// 
  /// This function may be freely refined.
  pub exec fn AES_128_GCM_DECRYPTS_LOG__developer_gumbox(
    encrypted_message: Common::EncryptedMessage_Impl,
    decrypted: Common::Log_Impl) -> (res: bool)
    ensures
      res == AES_128_GCM_DECRYPTS_LOG__developer_verus(encrypted_message, decrypted),
  {
    // This default implementation returns `true`, which is safe but weak:
    // * In `assume` contexts, returning `false` may allow GUMBOX to prove `false`.
    // * To obtain meaningful guarantees, developers should strengthen this
    //   specification to reflect the intended semantics of the GUMBO spec function.
    true
  }

  /// Developer-supplied GUMBOX realization of the GUMBO spec function `test`.
  /// 
  /// This function may be freely refined.
  pub exec fn AES_128_GCM_ENCRYPTS_RESPONSE__developer_gumbox(
    response: Common::Response_Impl,
    encrypted: Common::EncryptedMessage_Impl) -> (res: bool)
    ensures
      res == AES_128_GCM_ENCRYPTS_RESPONSE__developer_verus(response, encrypted),
  {
    // This default implementation returns `true`, which is safe but weak:
    // * In `assume` contexts, returning `false` may allow GUMBOX to prove `false`.
    // * To obtain meaningful guarantees, developers should strengthen this
    //   specification to reflect the intended semantics of the GUMBO spec function.
    true
  }

}
