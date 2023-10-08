use crate::ode::common::{ODE,collect_ode_result};
use crate::ode::{RK4 as Solver, RHSInput,RHSOutput,matlab};
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

#[wasm_bindgen]
extern "C" {
    fn ode_rhs(t:float,x:Vec<float>) -> Vec<float>;
}
#[wasm_bindgen]
pub fn ode4_r(step_size:float,x0:Vec<float>)->Result{
    let rhs=move |i:RHSInput<float>|{
        let t=i.t.clone();
        let x=i.x.to_vec();
        let out=ode_rhs(t,x);
        RHSOutput { dxdt: Array1::from_vec(out), signals: None }
    };
    let solver=Solver::new(rhs,Array1::from_vec(x0),step_size);
    Result::new(Box::new(solver))
}


#[wasm_bindgen]
pub fn ode4(f: &js_sys::Function,time:Vec<float>,x0:Vec<float>)->Data{
    let this = JsValue::null();
    let rhs=move |i:RHSInput<float>|{
        let t=i.t.clone();
        let x=i.x.to_vec();
        // let out=f.call2(&this,&JsValue::from_f64(t),&JsValue).unwrap();
        RHSOutput { dxdt: i.x.clone(), signals: None }
    };
    let (t, states, signals)=matlab::ode4(rhs, time.into(), Array1::from_vec(x0)).unwrap();
    let (names,data)=collect_ode_result(&t, &states, &signals, 0, t.len());
    Data{names,data}
}