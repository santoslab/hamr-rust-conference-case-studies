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
pub fn AGREE_Since(
  a: bool,
  b: bool,
  prev_result: bool) -> bool
{
  b ||
    a && prev_result
}
// END MARKER GUMBO RUST MARKER

verus! {

  // BEGIN MARKER GUMBO VERUS MARKER
  pub open spec fn AGREE_Since_spec(
    a: bool,
    b: bool,
    prev_result: bool) -> bool
  {
    b ||
      a && prev_result
  }
  // END MARKER GUMBO VERUS MARKER

}
