use ndarray::Array1;
use crate::ode::{RHSInput,RHSOutput,FloatScalar,RK4 as Solver};
use crate::plant::Integrator;
use crate::config::float;
use wasm_bindgen::prelude::wasm_bindgen;

#[wasm_bindgen]
struct Concensus<F>{
    solver:Solver<float,F>,
}