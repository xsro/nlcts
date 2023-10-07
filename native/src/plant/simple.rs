use ndarray::{Array1, s, ArrayView1, arr1};
use num::Float;

pub struct Integrator{
    order:usize,
}

impl Integrator{
    pub fn single()->Self{
        Self { order: 1 }
    }
    pub fn double()->Self{
        Self { order: 2 }
    }
    pub fn rhs<T:Float>(&self,u:T,states:ArrayView1<T>)->Result<Array1<T>,String>{
        if states.len()!=self.order{
            return Err(format!("{}!={}, states given to the agent is not same with order",states.len(),self.order))
        }
        let mut out=Array1::zeros(states.len());
        for i in 0..states.len()-1{
            out[i]=states[i+1];
        }
        out[states.len()-1]=u;
        return Ok(out)
    }
}

#[test]
fn test(){
    let a=Integrator::double();
    let da=a.rhs(0., ArrayView1::from(&[1.,2.])).unwrap();
    println!("{:#?}",da);
}