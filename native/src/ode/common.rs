use std::collections::BTreeMap;
use ndarray::{Array1,Array2};
use num::Float;

pub type SignalCollection<T>=BTreeMap<String,T>;


pub fn collect_ode_result<T:Float>(
    t:Vec<T>,states:Vec<Array1<T>>,
    signals:Vec<Option<SignalCollection<T>>>
)->(Vec<String>,Array2<T>){
    let mut names=vec!["simtime".to_string()];
    for i in 0..states[0].len(){
        names.push(format!("state_{}",i));
    }
    let states_len=names.len()-1;

    for i in 0..signals.len(){
        match &signals[i]{
            Some(sig) => {
                for key in sig.keys(){
                    if !names.contains(key){
                        names.push(format!("{}",key))
                    }
                }
            },
            None => {},
        };
    }
    
    
    let data=Array2::from_shape_fn((t.len(),names.len()), |(i,j)|{
        if j==0{
            t[i]
        }
        else if j-1<states_len {
            states[i][j-1]
        }
        else {
            let key=&names[j];
            match &signals[i]{
                Some(sig) => sig.get(key).unwrap_or(&T::nan()).clone(),
                None => T::nan(),
            }
        }
    });
    (names,data)
}

#[cfg(test)]
mod test{
    use ndarray::arr1;

    use super::*;
    #[test]
    fn test(){
        let t=vec![1.,2.,3.];
        let states=vec![
            arr1(&[1.,2.]),
            arr1(&[2.,2.]),
            arr1(&[1.,3.]),
            ];
        let mut sigs=BTreeMap::new();
        sigs.insert("u".to_string(), 1.);
        let signals=vec![
            None,
            Some(BTreeMap::new()),
            Some(sigs),
        ];
        let (names,data)=collect_ode_result(t, states, signals);
        println!("{:?}",names);
        println!("{:?}",data);
    }
}