use crate::{lf, config::float};
use super::ode::Result;

use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn concensus() -> Result{
    let x:Vec<float>=vec![1.,2.,3.];
    let solver=lf::concensus(x.clone(),1.);

    Result::new(Box::new(solver))
}