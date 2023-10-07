use std::vec;
use ndarray::Array1;
use super::common::{RHSInput,RHSOutput,FloatScalar};

/// Euler method for solving ODE
/// 
/// ## Implementation
/// 
/// Originally, I want to implement all data to Array2 and increase the size of the array as ode steps.
/// but this will move ode data, so I use Vec instead.
pub struct Euler<T:FloatScalar,F>
{
    pub step_size:T,
    pub states:Vec<Array1<T>>,
    pub times:Vec<T>,
    pub signals:Vec<RHSOutput<T>>,
    rhs:F,
}

impl<T:FloatScalar,F> Euler<T,F>
where F:for<'a> FnMut(RHSInput<'a,T>)->RHSOutput<T>
{
    pub fn new(rhs:F,initial:Array1<T>,step_size:T)->Self{
        Self{
            step_size,
            states:vec![initial],
            times:vec![T::zero()],
            signals:Vec::new(),
            rhs,
        }
    }
    fn init_or_finish_step(&mut self){
        let x=self.states.last().expect("states not initialized");
        let t=self.times.last().expect("time not initialized");
        let input=RHSInput{t,x,};
        let output=(self.rhs)(input);
        self.signals.push(output);
    }
    pub fn step(&mut self){
        if self.signals.len()==0 && self.signals.len()==0{
            self.init_or_finish_step();
        }
        
        let xn=self.states.last().expect("states not initialized");
        let tn=self.times.last().expect("time not initialized");
        let output=self.signals.last().expect("state change not initialized");

        let tn1=self.step_size+*tn;
        let xn1=output.dxdt.map(|x|{*x*self.step_size})+xn;

        self.times.push(tn1);
        self.states.push(xn1);

        self.init_or_finish_step()
    }
}




#[cfg(test)]
mod test{

    use super::*;

    /// test with scalar ode 
    /// dx=x*t 
    /// which analytically solution is
    /// x=exp(1/2*t^2)
    #[test]
    fn test(){
        let rhs=|i:RHSInput<'_, f64>|{
            let dx=i.x[0]*i.t;
            RHSOutput{dxdt:Array1::from_elem(1, dx),signals:None}
        };
        let initial=Array1::ones(1);
        let step_size=0.01f64;
        let mut solver=Euler::new(rhs,initial,step_size);

        let mut i=0;
        loop {
            solver.step();
            let t=solver.times.last().unwrap();
            let x=solver.states.last().unwrap()[0];
            let msg=format!("{:.2} {:.7} {:.7}",t,x,1.*(1./2.*t*t).exp());
            if i>10 { 
                assert_eq!(msg,String::from("0.12 1.0066193 1.0072260"));
                break;
            }
            else {i=i+1}
        }
    }
}