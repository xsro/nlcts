import * as THREE from "three";
import { Data } from "./Data.js";
import chroma from "chroma-js";
import { sci } from "./utils.js";
import katex from "katex";
import { GLTFLoader, GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";

import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { DragControls } from "three/examples/jsm/controls/DragControls.js";
// import { FlyControls } from "three/examples/jsm/controls/FlyControls.js";

async function load_model(url: string) {
  const loader = new GLTFLoader();
  const model = await loader.loadAsync(url);
  return model;
}

function lighter(child: any) {
  if (child.isMesh) {
    child.frustumCulled = false;
    //模型阴影
    child.castShadow = true;
    //模型自发光
    child.material.emissive = child.material.color;
    child.material.emissiveMap = child.material.map;
  }
}

async function load_agent(external: boolean) {
  if (external) {
    const jet = await load_model("hydra_jet__grand_theft_auto/scene.gltf");
    jet.scene.traverse(lighter);
    jet.scene.scale.set(0.1, 0.1, 0.1);
    return jet.scene;
  } else {
    const geometry = new THREE.CylinderGeometry(0.3, 0.3, 0.1);
    const material = new THREE.MeshBasicMaterial({
      color: chroma.random().hex(),
    });
    return new THREE.Mesh(geometry, material);
  }
}

async function load_target(external: boolean) {
  if (external) {
    const tank = await load_model("hcr2_tank/scene.gltf");
    tank.scene.traverse(lighter);
    tank.scene.scale.set(0.3, 0.3, 0.3);
    return tank.scene;
  } else {
    const geometry = new THREE.CylinderGeometry(0.2, 0.2, 0.1);
    const material = new THREE.MeshBasicMaterial({
      color: chroma.random().hex(),
    });
    return new THREE.Mesh(geometry, material);
  }
}

export async function threejsRender(
  data: Data,
  ele: HTMLElement,
  opt: {
    height: number;
    width: number;
    profile: { [id: string]: string };
  }
) {
  const eles = {
    t: document.createElement("span") as HTMLSpanElement,
    pause: document.createElement("button") as HTMLButtonElement,
    follow: document.createElement("input") as HTMLInputElement,
  };
  ele.append(...Object.values(eles));
  eles.t.className = "t";
  eles.pause.className = "right-top";
  eles.pause.innerText = "⏸";
  eles.follow.className = "left-bottom";
  eles.follow.type = "checkbox";

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    50,
    opt.width / opt.height,
    0.1,
    1000
  );

  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(opt.width, opt.height);
  ele.appendChild(renderer.domElement);

  //创建平行光
  const light = new THREE.PointLight(0xff0000, 1, 100);
  light.position.set(50, 50, 50);
  scene.add(light);
  scene.background = new THREE.Color(...chroma("gray").rgb());

  const clock = new THREE.Clock();
  clock.start();
  let last_render_idx = 0;

  //创建网格
  const gridHelper = new THREE.GridHelper(900, 100, 0x2c2c2c, 0x888888);
  scene.add(gridHelper);

  const initial = data[0].position;

  const target = await load_target(true);
  scene.add(target);
  target.position.set(initial.target.x, 0.5, initial.target.y);
  let target_final_pos = data[data.length - 1].position["target"];
  const d = opt.profile["neighbour_d"];
  const offset = parseFloat(d) * 1.6;
  camera.position.set(target_final_pos.x, 20, target_final_pos.y - offset);
  camera.lookAt(target.position);
  let orbitControl: OrbitControls | undefined = undefined;
  if (eles.follow.checked === false) {
    //创建控件;
    orbitControl = new OrbitControls(camera, renderer.domElement);
    const dragControl = new DragControls([camera], camera, renderer.domElement);
    // const flyControl = new FlyControls(camera, renderer.domElement);
  }

  const followers: { [id: string]: THREE.Group } = {};
  // const moving_target = opt.profile["target"].split(" ").length == 4;
  Object.entries(initial).map(async ([name, pos], idx) => {
    if (name == "target") return;
    const agent = await load_agent(true);
    scene.add(agent);
    followers[name] = agent as THREE.Group;
  });

  let paused = false;
  eles.pause.addEventListener("click", () => {
    paused = !paused;
    eles.pause.innerText = paused ? "▶️" : "⏸";
    if (paused) clock.stop();
    else clock.start();
  });

  function animate() {
    const id = requestAnimationFrame(animate);
    const t = clock.getElapsedTime();

    if (!paused) {
      if (last_render_idx >= data.length - 3) {
        // cancelAnimationFrame(id);
        return;
      }
      if (t < data[last_render_idx].t) {
        return;
      }
      while (t > data[last_render_idx].t && last_render_idx < data.length - 1) {
        last_render_idx += 1;
      }
      const t_expr = "t=" + sci(t, 2);
      katex.render(t_expr, eles.t, { throwOnError: true });

      for (const agentname of Object.keys(followers)) {
        if (data[last_render_idx].position[agentname] == undefined) continue;
        const pos = data[last_render_idx].position[agentname];
        const agent = followers[agentname];
        const agent_pos = new THREE.Vector3(pos.x, 0.7, pos.y);
        agent.position.set(agent_pos.x, agent_pos.y, agent_pos.z);
        const pos_next = data[last_render_idx + 1].position[agentname];
        agent.lookAt(-pos_next.x, 0.7, -pos_next.y);
      }

      const pos = data[last_render_idx].position["target"];
      target.position.set(pos.x, 0, pos.y);
      const pos_next = data[last_render_idx + 1].position["target"];
      target.lookAt(pos_next.x, 0, pos_next.y);

      if (eles.follow.checked == true) {
        camera.position.set(target.position.x, 10, target.position.y);
        camera.lookAt(target.position);
        if (orbitControl) {
          orbitControl.enabled = false;
        }
      } else if (orbitControl) {
        orbitControl.enabled = true;
        orbitControl.target.set(...target.position.toArray());
        orbitControl.update();
      }
    }
    renderer.render(scene, camera);
  }
  animate();
}
