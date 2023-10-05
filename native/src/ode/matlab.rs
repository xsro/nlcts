use std::collections::BTreeMap;

use ndarray::Array1;
use num::Float;
use super::{RK4,Euler};




pub fn ode2<T,F>(rhs:F,t:Array1<T>,initial:Array1<T>)->Result<(),String>
where 
    T:Float,
    F:for<'a> FnMut(&'a T,&'a Array1<T>)->(Array1<T>,Option<BTreeMap<String,T>>)
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
    Ok(())
}