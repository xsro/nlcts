import * as ace from "ace-builds"
import "ace-builds/src-noconflict/theme-monokai"
import "ace-builds/src-noconflict/mode-javascript"

import * as nlct from "nlct"

import Plotly from 'plotly.js-dist-min'


var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/javascript");
editor.setOption("useWorker", false);

(window as any).ode_rhs=function (t:number,x:number[]):number[]{
    let rhsText=editor.getValue();
    let custom_rhs=new Function("t","x",rhsText+"return rhs(t,x).dxdt");
    return custom_rhs(t,x);
};

let simulation_index=0;

(window as any).simulation_run=function(realtime:boolean){
    let id=++simulation_index;
    let rhsText=editor.getValue();
    let opt=new Function("t","x",rhsText+"return odeOption;")();
    let s=nlct.ode4_r(opt.tstep,Float64Array.from(opt.x0));

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
            title:'all signals',
        };

        Plotly.newPlot('inspector', plot_data, layout);
    },
    realtime?opt.tstep*1000:undefined)
};

(window as any).simulation_stop=function(){
    simulation_index++;
};
