import React, { useRef } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { TextureLoader, DoubleSide } from 'three';

export default function Clouds() {
    const cloudsRef = useRef();

    const cloudMap = useLoader(TextureLoader, '/textures/04_earthcloudmap.jpg');
    const cloudTransMap = useLoader(TextureLoader, '/textures/05_earthcloudmaptrans.jpg');

    useFrame(() => {
        if (cloudsRef.current) {
        cloudsRef.current.rotation.y += 0.0005;
        }
    });

    return (
        <mesh ref={cloudsRef}>
        <sphereGeometry args={[1.01, 64, 64]} /> {/* Slightly bigger than earth */}
        <meshPhongMaterial
            map={cloudMap}
            alphaMap={cloudTransMap}
            transparent={true}
            depthWrite={false}
            side={DoubleSide}
            opacity={0.8}
        />
        </mesh>
    );
}
