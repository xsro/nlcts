use ndarray::Array1;
use crate::ode::{RHSInput,RHSOutput,RK4 as Solver};
use crate::config::float;

pub fn concensus(x:Vec<float>,gain:float,)->Solver<float,impl FnMut(RHSInput<'_,float>)->RHSOutput<float>>{
    Solver::new(
        move |input:RHSInput<float>|{
            let mut dxdt=Array1::zeros(input.x.len());
            for i in 0..input.x.len(){
                let mut sum=0.0;
                for j in 0..input.x.len(){
                    sum+=gain*(input.x[j]-input.x[i]);
                }
                dxdt[i]=sum;
            }
            RHSOutput{dxdt,signals:None}
        },
        Array1::from_vec(x.clone()),
        0.01,
    )
}

#[test]
fn test(){
    let x=vec![1.,2.,3.];
    let mut solver=concensus(x.clone(),1.);

    let ave=Array1::from_vec(x.clone()).sum()/(x.len() as float);
    loop {
        solver.step();
        let t=solver.times.last().unwrap();
        let x=solver.states.last().unwrap();
        let e=(x[0]-ave).abs();
        if e<1e-10{
            break;
        }
        else{
            println!("t={},x1-ave(x)={:e}",t,e)
        }
    }
}