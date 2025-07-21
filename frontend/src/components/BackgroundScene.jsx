import React, { useRef } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import { getFresnelMat } from '../three/getFresnelMat';
import '../styles/components/backgroundScene.css';
import Stars from './Stars'; // Add this import


function EarthWithGlow() {
    const colorMap = useLoader(THREE.TextureLoader, '/textures/00_earthmap1k.jpg');
    const bumpMap = useLoader(THREE.TextureLoader, '/textures/01_earthbump1k.jpg');
    const specMap = useLoader(THREE.TextureLoader, '/textures/02_earthspec1k.jpg');
    const nightMap = useLoader(THREE.TextureLoader, '/textures/03_earthlights1k.jpg');
    const cloudMap = useLoader(THREE.TextureLoader, '/textures/04_earthcloudmap.jpg');
    const cloudTrans = useLoader(THREE.TextureLoader, '/textures/05_earthcloudmaptrans.jpg');

    const earthRef = useRef();
    const cloudsRef = useRef();
    const glowRef = useRef();

    useFrame(() => {
        earthRef.current.rotation.y += 0.0015;
        cloudsRef.current.rotation.y += 0.001;
        glowRef.current.rotation.y += 0.0015;
    });

    return (
        <group>
        {/* Earth Sphere */}
        <mesh ref={earthRef}>
            <sphereGeometry args={[1, 64, 64]} />
            <meshPhongMaterial
            map={colorMap}
            bumpMap={bumpMap}
            bumpScale={0.05}
            specularMap={specMap}
            specular={new THREE.Color('grey')}
            emissiveMap={nightMap}
            emissive={new THREE.Color('white')}
            emissiveIntensity={0.6}
            />
        </mesh>

        {/* Cloud Layer */}
        <mesh ref={cloudsRef}>
            <sphereGeometry args={[1.01, 64, 64]} />
            <meshPhongMaterial
            map={cloudMap}
            alphaMap={cloudTrans}
            transparent={true}
            depthWrite={false}
            side={THREE.DoubleSide}
            />
        </mesh>

        {/* Fresnel Glow */}
        <mesh ref={glowRef}>
            <sphereGeometry args={[1.02, 64, 64]} />
            <primitive object={getFresnelMat()} attach="material" />
        </mesh>
        </group>
    );
}


export default function BackgroundScene() {
    return (
        <div className="background-scene">
        <Canvas camera={{ position: [0, 0, 3] }}>
            <ambientLight intensity={0.5} />
            <directionalLight position={[5, 5, 5]} intensity={1} />

            <Stars />         {/* ✨ Add starfield */}
            <EarthWithGlow /> {/* 🌍 Earth with glow & clouds */}

            <OrbitControls enableZoom={false} />
        </Canvas>
        </div>
    );
}
