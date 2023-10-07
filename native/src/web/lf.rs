use ndarray::Array1;

use crate::{lf, config::float};
use super::ode::Result;

use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn concensus() -> Result{
    let x=vec![1.,2.,3.];
    let mut solver=lf::concensus(x.clone(),1.);

    Result::new(Box::new(solver))
}