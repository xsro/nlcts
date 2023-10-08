import * as nlct from "nlct"

export function test(){
    

    (window as any).ode_rhs=function(x:number[],t:number){
        console.log(x,t)
        return x
    }
    let s=nlct.ode4_r(0.1,Float64Array.from([1,2]));
    s.step()
    debugger
    test1();
}

function test1(){
    let s=nlct.concensus();
    s.step()
    let data=s.last_data();
    let ini=Date.now();
    function call(){
        for (let i=0;i<100;i++)
            s.step()
        data=s.last_data();
        let names=data.names().split(",")
        let data_array=data.data()
        let data_object:any={now:(Date.now()-ini)/1000}
        for (let i=0;i<names.length;i++){
            data_object[names[i]]=data_array[i]
        }
        console.table(data_object)
    }
    setInterval(call,1000);
}