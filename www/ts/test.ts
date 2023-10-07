import * as nlct from "nlct"

export function test(){
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
    setInterval(call,1000)
    
}