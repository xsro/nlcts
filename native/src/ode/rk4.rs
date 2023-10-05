use std::vec;
use num::Float;
use ndarray::Array1;
use super::common::SignalCollection;

pub struct RK4<T,F>
{
    pub step_size:T,
    pub states:Vec<Array1<T>>,
    pub times:Vec<T>,
    pub signals:Vec<Option<SignalCollection<T>>>,
    pub state_changes:Vec<Array1<T>>,
    rhs:F,
}

impl<T:Float+ndarray::ScalarOperand,F> RK4<T,F>
where F:for<'a> FnMut(&'a T,&'a Array1<T>)->(Array1<T>,Option<SignalCollection<T>>)
{
    pub fn new(rhs:F,initial:Array1<T>,step_size:T)->Self{
        Self{
            step_size,
            states:vec![initial],
            times:vec![T::zero()],
            signals:Vec::new(),
            rhs,
            state_changes:Vec::new(),
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

        let two=T::one()+T::one();
        let six=two+two+two;
        let xn=self.states.last().expect("states not initialized");
        let tn=self.times.last().expect("time not initialized");
        let f1=self.state_changes.last().expect("state change not initialized");
        let k1=f1*self.step_size;

        let t=self.step_size/two+*tn;
        let x=xn+&k1/two;
        let (f,_)=(self.rhs)(&t,&x);
        let k2=f*self.step_size;

        let t=self.step_size/two+*tn;
        let x=xn+&k2/two;
        let (f,_)=(self.rhs)(&t,&x);
        let k3=f*self.step_size;

        let t=self.step_size+*tn;
        let x=xn+&k3;
        let (f,_)=(self.rhs)(&t,&x);
        let k4=f*self.step_size;

        let tn1=self.step_size+*tn;
        let xn1=(k1+k2*two+k3*two+k4)/six+xn;

        self.times.push(tn1);
        self.states.push(xn1);
        self.init_or_finish_step();
        
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
        let mut solver=RK4::new(rhs,initial,step_size);

        let mut i=0;
        loop {
            solver.step();
            let t=solver.times.last().unwrap();
            let x=solver.states.last().unwrap()[0];
            let msg=format!("{:.2} {:.7} {:.7}",t,x,1.*(1./2.*t*t).exp());
            if i>10 { 
                assert_eq!(msg,String::from("0.12 1.0072260 1.0072260"));
                break;
            }
            else {i=i+1}
        }
    }
}