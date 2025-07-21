import React, { useMemo, useRef } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import * as THREE from 'three';

export default function Stars() {
    const texture = useLoader(THREE.TextureLoader, '/textures/star.png');
    const starsRef = useRef();

    const starGeometry = useMemo(() => new THREE.BufferGeometry(), []);
    const starMaterial = useMemo(() => {
        return new THREE.PointsMaterial({
        size: 2.0,               // star size
        sizeAttenuation: true,   // make size perspective-correct
        map: texture,            // use the circular texture
        alphaTest: 0.5,          // discard pixels below this alpha
        transparent: true,
        color: new THREE.Color(0xffffff),
        });
    }, [texture]);

    // generate random positions
    useMemo(() => {
        const starVertices = [];
        for (let i = 0; i < 5000; i++) {
        const x = THREE.MathUtils.randFloatSpread(2000);
        const y = THREE.MathUtils.randFloatSpread(2000);
        const z = THREE.MathUtils.randFloatSpread(2000);
        starVertices.push(x, y, z);
        }
        starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
    }, [starGeometry]);

    // animate rotation
    useFrame(() => {
        if (starsRef.current) {
        starsRef.current.rotation.y += 0.0002;
        }
    });

    return <points ref={starsRef} geometry={starGeometry} material={starMaterial} />;
}
