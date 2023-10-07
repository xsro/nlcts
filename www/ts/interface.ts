import GUI from 'lil-gui';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export class Render{
    
    constructor(
        public parent:HTMLDivElement,
        public gui:GUI){
    }

    bind(){
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

        const renderer = new THREE.WebGLRenderer();
        renderer.setSize( window.innerWidth, window.innerHeight );
        this.parent.appendChild( renderer.domElement );

        const axeshelper=new THREE.AxesHelper()
        scene.add(axeshelper);

        const gridhelper=new THREE.GridHelper()
        scene.add(gridhelper)
        
        const control=new OrbitControls(camera,renderer.domElement)

        camera.position.z = 5;

        function animate() {
            requestAnimationFrame( animate );

            renderer.render( scene, camera );
        }
        animate();    
    }
}