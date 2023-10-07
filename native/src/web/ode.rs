use crate::ode::common::{ODE,RHSOutput,collect_ode_result};
use ndarray::{Array1, Array2};
use crate::config::float;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct Result{
    i:Box<dyn ODE<float>>,
}

impl Result{
    pub fn new(i:Box<dyn ODE<float>>)->Self{
        Self{i}
    }
}


impl ODE<float> for Result{
    fn step(&mut self){
        self.i.step();
    }
    fn get_times(&self)->&Vec<float>{
        self.i.get_times()
    }
    fn get_states(&self)->&Vec<Array1<float>>{
        self.i.get_states()
    }
    fn get_signals(&self)->&Vec<RHSOutput<float>>{
        self.i.get_signals()
    }
}

#[wasm_bindgen]
pub struct Data{
    names:Vec<String>,
    data:Array2<float>,
}

#[wasm_bindgen]
impl Data{
    pub fn names(&self)->String{
        self.names.join(", ")
    }
    pub fn data(&self)->Vec<float>{
        let mut out=Vec::new();
        for i in 0..self.data.nrows(){
            for j in 0..self.data.ncols(){
                out.push(self.data[[i,j]]);
            }
        }
        out
    }
}

#[wasm_bindgen]
impl Result{
    pub fn step(&mut self){
        self.i.step();
    }
    pub fn times(&self)->Vec<float>{
        self.i.get_times().clone()
    }
    pub fn last_data(&self)->Data{
        self.data(self.i.get_times().len()-1)
    }
    pub fn data(&self,index:usize)->Data{
        let t=self.get_times();
        let states=self.get_states();
        let signals=self.get_signals();
        let from=index;
        let to=index+1;
        let (names,data)=collect_ode_result(t, states, signals, from, to);
        Data{names,data}
    }
}