use num::Float;

/// Pendulum model
/// ddtheta+sin theta + b dtheta =cu
struct Pendulum<T>{
    b:T,
    c:T,
}

pub struct State<T>{
    pub x1:T,
    pub x2:T,
}


impl<T:Float> Pendulum<T>{
    fn new(b:T,c:T)->Self{
        Self{
            b,
            c,
        }
    }
    fn rhs(&self,u:T,v:T)->(T,T){
        (v,-self.b*v-self.c*u)
    }
}