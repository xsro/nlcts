mod ode;
mod lf;

use wasm_bindgen::prelude::*;

#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet() {
    alert("Hello, nlct!");
}

#[wasm_bindgen]
pub fn nlct(){

}