use std::vec;
use ndarray::Array1;
use super::common::{RHSInput,RHSOutput,FloatScalar,ODE};

pub struct RK4<T:FloatScalar,F>
{
    pub step_size:T,
    pub states:Vec<Array1<T>>,
    pub times:Vec<T>,
    pub signals:Vec<RHSOutput<T>>,
    rhs:F,
}

// trait RHS<T>= for<'a> FnMut(&'a T,&'a Array1<T>)->(Array1<T>,Option<SignalCollection<T>>);

impl<T:FloatScalar,F> RK4<T,F>
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

        let two=T::one()+T::one();
        let six=two+two+two;
        let xn=self.states.last().expect("states not initialized");
        let tn=self.times.last().expect("time not initialized");
        let f1=&self.signals.last().expect("state change not initialized").dxdt;
        let k1=f1*self.step_size;

        let t=self.step_size/two+*tn;
        let x=xn+&k1/two;
        let f=(self.rhs)(RHSInput::new(&t,&x)).dxdt;
        let k2=f*self.step_size;

        let t=self.step_size/two+*tn;
        let x=xn+&k2/two;
        let f=(self.rhs)(RHSInput::new(&t,&x)).dxdt;
        let k3=f*self.step_size;

        let t=self.step_size+*tn;
        let x=xn+&k3;
        let f=(self.rhs)(RHSInput::new(&t,&x)).dxdt;
        let k4=f*self.step_size;

        let tn1=self.step_size+*tn;
        let xn1=(k1+k2*two+k3*two+k4)/six+xn;

        self.times.push(tn1);
        self.states.push(xn1);
        self.init_or_finish_step();
        
    }
}

impl<T:FloatScalar,F> ODE<T> for RK4<T,F>
where F:for<'a> FnMut(RHSInput<'a,T>)->RHSOutput<T>
{
    fn step(&mut self){
        self.step();
    }
    fn get_states(&self)->&Vec<Array1<T>>{
        &self.states
    }
    fn get_times(&self)->&Vec<T>{
        &self.times
    }
    fn get_signals(&self)->&Vec<RHSOutput<T>>{
        &self.signals
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