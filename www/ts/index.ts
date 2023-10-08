import * as ace from "ace-builds"
import "ace-builds/src-noconflict/theme-monokai"
import "ace-builds/src-noconflict/mode-javascript"

import * as nlct from "nlct"

import Plotly from 'plotly.js-dist-min'


let default_rhs_text=`
//set initial state, step size and other options here
let odeOption={
    x0:[Math.PI/2,0],
    tstep:0.1,
}

//define the right hand side of the ode equation here
function rhs(t,x) {
    let x1=x[0],x2=x[1];
    let r=Math.sin(t/3);
    let dr=Math.cos(t/3)/3;
    let ddr=-Math.sin(t/3)/9;
    let b=0.03,c=1;
    let k1=1,k2=1;

    let e1=x1-r;
    let e2=x2-dr;
    let u=1/c*(Math.sin(x1)+b*x2+ddr-k1*e1-k2*e2);
    let dx1=x2;
    let dx2=-Math.sin(x1)-b*x2+c*u;
    let dxdt=[dx1,dx2];
    return {dxdt};
}
`;

var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/javascript");
editor.setOption("useWorker", false);
editor.setValue(default_rhs_text,9);
let ode_rhs=function (t:number,x:number[]):number[]{
    let rhsText=editor.getValue();
    let custom_rhs=new Function("t","x",rhsText+"return rhs(t,x).dxdt");
    return custom_rhs(t,x);
};
(window as any).ode_rhs=ode_rhs;

let simulation_index=0;

(window as any).simulation_run=function(realtime:boolean){
    let id=++simulation_index;
    let rhsText=editor.getValue();
    let opt=new Function("t","x",rhsText+"return odeOption;")();
    let s=nlct.ode4_r(opt.tstep,Float64Array.from(opt.x0));
    try{
        ode_rhs(0,opt.x0)
    }
    catch(e){
        alert("rhs function error: "+e);
        debugger;
        return;
    }
    const datas:{[id:string]:number[]}={};
    const iid=setInterval(()=>{
        if (id!=simulation_index) clearInterval(iid);
        s.step()
        let last=s.last_data();
        let names=last.names().split(",");
        let data=last.data();
        for (let i=0;i<names.length;i++){
            if(datas[names[i]]==undefined) {
                datas[names[i]]=[]
            }
            else{
                datas[names[i]].push(data[i]);
            }
        }
        let plot_data = [];
        for (let name in datas){
            if(name==="simtime") continue;
            plot_data.push({
                x:datas['simtime'],
                y:datas[name],
                name:name,
            });
        }

        let layout = {
            title:"t="+data[0].toFixed(2),
        };

        Plotly.newPlot('inspector', plot_data, layout);
    },
    realtime?opt.tstep*1000:0)
};

(window as any).simulation_stop=function(){
    simulation_index++;
};
