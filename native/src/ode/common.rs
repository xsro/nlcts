use std::collections::BTreeMap;
use ndarray::{Array1,Array2,ScalarOperand};
use num::Float;

pub type SignalCollection<T>=BTreeMap<String,T>;
pub trait FloatScalar:Float+ScalarOperand{}
impl FloatScalar for f32{}
impl FloatScalar for f64{}

// trait alias is not ready yet so we just define the input type here
pub struct RHSInput<'a,T:FloatScalar>{
    pub t:&'a T,
    pub x:&'a Array1<T>,
}

impl<'a,T:FloatScalar> RHSInput<'a,T>{
    pub fn new(t:&'a T,x:&'a Array1<T>)->Self{
        Self{t,x}
    }
}

// trait alias is not ready yet so we just define the return type here
pub struct RHSOutput<T:FloatScalar>{
    pub dxdt:Array1<T>,
    pub signals:Option<SignalCollection<T>>,
}

pub trait ODE<T:FloatScalar>{
    fn step(&mut self);
    fn get_states(&self)->&Vec<Array1<T>>;
    fn get_times(&self)->&Vec<T>;
    fn get_signals(&self)->&Vec<RHSOutput<T>>;
}


/// return all signals to Array2
pub fn collect_ode_result<T:FloatScalar>(
    t:&Vec<T>,
    states:&Vec<Array1<T>>,
    signals:&Vec<RHSOutput<T>>,
    from:usize,
    to:usize,
)->(Vec<String>,Array2<T>){
    //collect all signal names
    let mut signal_names=Vec::new();
    for i in from..to{
        match &signals[i].signals{
            Some(sig) => {
                for key in sig.keys(){
                    if !signal_names.contains(key){
                        signal_names.push(format!("{}",key))
                    }
                }
            },
            None => {},
        };
    }

    let mut names=vec!["simtime".to_string()];
    for i in 0..states[from].len(){
        names.push(format!("x_{}",i));
    }
    let states_len=names.len()-1;
    for i in 0..states[from].len(){
        names.push(format!("dx_{}",i));
    }
    names.append(&mut signal_names);
    
    let data=Array2::from_shape_fn((to-from,names.len()), |(_i,j)|{
        let i=_i+from;
        if j==0{
            t[i]
        }
        else if j-1<states_len {
            states[i][j-1]
        }
        else if j-1<states_len*2 {
            signals[i].dxdt[j-1-states_len]
        }
        else {
            let key=&names[j];
            match &signals[i].signals{
                Some(sig) => sig.get(key).unwrap_or(&T::nan()).clone(),
                None => T::nan(),
            }
        }
    });
    (names,data)
}

#[cfg(test)]
mod test{
    use ndarray::arr1;
    use super::*;
    #[test]
    fn test(){
        let t=vec![1.,2.,3.];
        let states=vec![
            arr1(&[1.,2.]),
            arr1(&[2.,2.]),
            arr1(&[1.,3.]),
            ];
        let mut sigs=BTreeMap::new();
        sigs.insert("u".to_string(), 1.);
        let signals=vec![
            RHSOutput{dxdt:arr1(&[10.,20.]),signals:None},
            RHSOutput{dxdt:arr1(&[10.,20.]),signals:Some(BTreeMap::new())},
            RHSOutput{dxdt:arr1(&[10.,20.]),signals:Some(sigs)},
        ];
        let (names,data)=collect_ode_result(&t, &states, &signals,0,2);
        println!("{:?}",names);
        println!("{:?}",data);
    }
}