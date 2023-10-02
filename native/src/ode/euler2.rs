use std::vec;
use num::Float;
use ndarray::Array1;
use std::collections::BTreeMap;

pub struct Euler<T,F>
{
    pub step_size:T,
    pub states:Vec<Array1<T>>,
    pub times:Vec<T>,
    pub signals:Vec<Option<BTreeMap<String,T>>>,
    pub state_changes:Vec<Array1<T>>,
    rhs:F,
}

impl<T:Float,F> Euler<T,F>
where F:for<'a> FnMut(&'a T,&'a Array1<T>)->(Array1<T>,Option<BTreeMap<String,T>>)
{
    pub fn new(rhs:F,initial:Array1<T>,step_size:T)->Self{
        Self{
            step_size,
            states:vec![initial],
            times:vec![T::zero()],
            signals:Vec::new(),
            state_changes:Vec::new(),
            rhs,
        }
    }
    fn init_or_finish_step(&mut self){
        let xn=self.states.last().expect("states not initialized");
        let tn=self.times.last().expect("time not initialized");

        let (change,signal)=(self.rhs)(&tn,&xn);
        
        self.state_changes.push(change);
        self.signals.push(signal);
    }
    pub fn step(&mut self){
        if self.signals.len()==0 && self.state_changes.len()==0{
            self.init_or_finish_step();
        }
        
        let xn=self.states.last().expect("states not initialized");
        let tn=self.times.last().expect("time not initialized");

        let (f,s)=(self.rhs)(&tn,xn);

        let tn1=self.step_size+*tn;
        let xn1=f.map(|x|{*x*self.step_size})+xn;

        self.times.push(tn1);
        self.states.push(xn1);
        self.signals.push(s);
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
        let rhs=|t:&f64,x:&Array1<f64>|{
            let dx=x[0]*t;
            (Array1::from_elem(1, dx),None)
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