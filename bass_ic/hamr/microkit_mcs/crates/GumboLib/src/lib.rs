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
pub fn isMalformedFrame(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.malformedFrame
}

pub fn getInternetProtocol(v: SW::StructuredEthernetMessage_i) -> SW::InternetProtocol
{
  v.internetProtocol
}

pub fn isIPV4(v: SW::StructuredEthernetMessage_i) -> bool
{
  getInternetProtocol(v) == SW::InternetProtocol::IPV4
}

pub fn isIPV6(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.internetProtocol == SW::InternetProtocol::IPV6
}

pub fn getFrameProtocol(v: SW::StructuredEthernetMessage_i) -> SW::FrameProtocol
{
  v.frameProtocol
}

pub fn isTCP(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.frameProtocol == SW::FrameProtocol::TCP
}

pub fn isARP(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.frameProtocol == SW::FrameProtocol::ARP
}

pub fn isPortWhitelisted(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.portIsWhitelisted
}

pub fn getARP_Type(v: SW::StructuredEthernetMessage_i) -> SW::ARP_Type
{
  v.arpType
}

pub fn isARP_Request(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.arpType == SW::ARP_Type::REQUEST
}

pub fn isARP_Reply(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.arpType == SW::ARP_Type::REPLY
}

pub fn isGeofenceViolation(v: SW::StructuredEthernetMessage_i) -> bool
{
  v.rawMessage[0] == 0u8
}

pub fn isAttack(v: SW::AttackStatus) -> bool
{
  v == SW::AttackStatus::Attack
}

pub fn rxShouldPass(v: SW::StructuredEthernetMessage_i) -> bool
{
  !(isMalformedFrame(v)) & isIPV4(v) &
    isTCP(v) &
    isPortWhitelisted(v)
}

pub fn txExpected(v: SW::StructuredEthernetMessage_i) -> bool
{
  isIPV4(v) | isARP(v)
}
// END MARKER GUMBO RUST MARKER

verus! {

  // BEGIN MARKER GUMBO VERUS MARKER
  pub open spec fn isMalformedFrame_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.malformedFrame
  }

  pub open spec fn getInternetProtocol_spec(v: SW::StructuredEthernetMessage_i) -> SW::InternetProtocol
  {
    v.internetProtocol
  }

  pub open spec fn isIPV4_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    getInternetProtocol_spec(v) == SW::InternetProtocol::IPV4
  }

  pub open spec fn isIPV6_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.internetProtocol == SW::InternetProtocol::IPV6
  }

  pub open spec fn getFrameProtocol_spec(v: SW::StructuredEthernetMessage_i) -> SW::FrameProtocol
  {
    v.frameProtocol
  }

  pub open spec fn isTCP_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.frameProtocol == SW::FrameProtocol::TCP
  }

  pub open spec fn isARP_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.frameProtocol == SW::FrameProtocol::ARP
  }

  pub open spec fn isPortWhitelisted_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.portIsWhitelisted
  }

  pub open spec fn getARP_Type_spec(v: SW::StructuredEthernetMessage_i) -> SW::ARP_Type
  {
    v.arpType
  }

  pub open spec fn isARP_Request_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.arpType == SW::ARP_Type::REQUEST
  }

  pub open spec fn isARP_Reply_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.arpType == SW::ARP_Type::REPLY
  }

  pub open spec fn isGeofenceViolation_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    v.rawMessage[0] == 0u8
  }

  pub open spec fn isAttack_spec(v: SW::AttackStatus) -> bool
  {
    v == SW::AttackStatus::Attack
  }

  pub open spec fn rxShouldPass_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    ((!(isMalformedFrame_spec(v)) && isIPV4_spec(v)) &&
      isTCP_spec(v)) &&
      isPortWhitelisted_spec(v)
  }

  pub open spec fn txExpected_spec(v: SW::StructuredEthernetMessage_i) -> bool
  {
    isIPV4_spec(v) || isARP_spec(v)
  }
  // END MARKER GUMBO VERUS MARKER

}
