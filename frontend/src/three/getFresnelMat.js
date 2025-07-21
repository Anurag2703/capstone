import * as THREE from 'three';

export function getFresnelMat() {
  return new THREE.ShaderMaterial({
    uniforms: {
      color: { value: new THREE.Color(0x00ffff) }, // glow color
      power: { value: 2.0 }
    },
    vertexShader: `
      varying vec3 vNormal;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      varying vec3 vNormal;
      uniform vec3 color;
      uniform float power;
      void main() {
        float intensity = pow(1.0 - abs(vNormal.z), power);
        gl_FragColor = vec4(color, intensity);
      }
    `,
    transparent: true,
    side: THREE.FrontSide,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });
}
