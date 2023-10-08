use ndarray::Array1;
use super::{RK4,Euler, RHSOutput,FloatScalar,RHSInput};


type OdeResult<T>=(Vec<T>,Vec<Array1<T>>,Vec<RHSOutput<T>>);

pub fn ode2<T,F>(rhs:F,t:Array1<T>,initial:Array1<T>)->Result<OdeResult<T>,String>
where 
    T:FloatScalar,
    F:for<'a> FnMut(RHSInput<'a,T>)->RHSOutput<T>
{
    if t.len()<2{
        return Err("third parameter `t` should has at least two element".to_string());
    }
    let mut solver=Euler::new(rhs,initial,t[1]-t[0]);
    solver.step();
    for i in 1..t.len()-1{
        solver.step_size=t[i]-t[i-1];
        solver.step();
    }
    Ok((solver.times,solver.states,solver.signals))
}

pub fn ode4<T,F>(rhs:F,t:Array1<T>,initial:Array1<T>)->Result<OdeResult<T>,String>
where 
    T:FloatScalar,
    F:for<'a> FnMut(RHSInput<'a,T>)->RHSOutput<T>
{
    if t.len()<2{
        return Err("third parameter `t` should has at least two element".to_string());
    }
    let mut solver=RK4::new(rhs,initial,t[1]-t[0]);
    solver.step();
    for i in 1..t.len()-1{
        solver.step_size=t[i]-t[i-1];
        solver.step();
    }
    Ok((solver.times,solver.states,solver.signals))
}