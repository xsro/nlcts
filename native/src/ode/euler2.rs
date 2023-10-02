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
            rhs,
        }
    }
    pub fn step(&mut self){
        let xn=self.states.last().expect("states not initialized");
        let tn=self.times.last().expect("time not initialized");

        let (f,s)=(self.rhs)(&tn,xn);

        let tn1=self.step_size+*tn;
        let xn1=f.map(|x|{*x*self.step_size})+xn;

        self.times.push(tn1);
        self.states.push(xn1);
        self.signals.push(s);
    }
}




#[cfg(test)]
mod test{
    use super::*;

    #[test]
    fn test(){
        let rhs=|t:&f64,x:&Array1<f64>|{
            (Array1::from_elem(1, 0.1),None)
        };
        let initial=Array1::zeros(1);
        let step_size=0.1f64;
        let mut solver=Euler::new(rhs,initial,step_size);

        let mut i=0;
        loop {
            solver.step();
            let t=solver.times.last().unwrap();
            let x=solver.states.last().unwrap()[0];
            println!("{:.2} {:.2}",t,x);
            if i>10 { 
                assert_eq!(format!("{:.2} {:.2}",t,x),String::from("1.20 0.12"));
                break;
            }
            else {i=i+1}
        } 
    }
}