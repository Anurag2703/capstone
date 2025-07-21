import React, { useRef } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';

export default function Earth() {
    const earthRef = useRef();

    const [colorMap, bumpMap, specularMap] = useLoader(TextureLoader, [
        '/textures/00_earthmap1k.jpg',
        '/textures/01_earthbump1k.jpg',
        '/textures/02_earthspec1k.jpg'
    ]);

    useFrame(() => {
        if (earthRef.current) {
        earthRef.current.rotation.y += 0.001;
        }
    });

    return (
        <mesh ref={earthRef}>
        <sphereGeometry args={[1, 64, 64]} />
        <meshPhongMaterial
            map={colorMap}
            bumpMap={bumpMap}
            bumpScale={0.05}
            specularMap={specularMap}
            specular={[0.2, 0.2, 0.2]}
        />
        </mesh>
    );
}
