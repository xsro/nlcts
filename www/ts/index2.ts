import GUI from 'lil-gui';
import { Render } from './interface.js';
import { test } from './test.js';

const gui = new GUI();

enum Profile{
  empty=0,
  JustRender=1,
}

const guiConfig = {
  profile:0,
	myBoolean: true,
	myFunction: function() {  },
	myString: 'lil-gui',
	myNumber: 1
};

gui.add( guiConfig, 'profile', {
  "empty": Profile.empty,
 } );


async function render(profile:Profile,p:HTMLDivElement,gui:GUI){
  if (profile==Profile.empty){
    const r=new Render(p,gui)
    r.bind()
  }
}


async function main(){
  const p=document.getElementsByClassName("playground")[0] as HTMLDivElement
  if(p===undefined) throw new Error("Canvas not found")

  const url=window.location.href
  const searchparams=new URL(url).searchParams
  let profile=Profile.empty
  if (searchparams.has("profile")){
    try{
      profile=parseInt(searchparams.get("profile") as string)
    }catch{
      console.log("searchparams ignored",searchparams.get("profile"))
    }
  }

  render(profile,p,gui)
  let lastProfile:undefined|Profile=undefined
  gui.onFinishChange(event=>{
    const profile=(event.object as typeof guiConfig)["profile"]
    if(lastProfile!==profile){
      p.style.background="gray"
      lastProfile=profile
      render(profile,p,gui)
    }
  })
}

test()
main()