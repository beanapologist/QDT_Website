declare module 'three' {
  export class Scene {
    add(object: any): void;
  }

  export class PerspectiveCamera {
    constructor(fov: number, aspect: number, near: number, far: number);
    position: { z: number };
    aspect: number;
    updateProjectionMatrix(): void;
  }

  export class WebGLRenderer {
    constructor(options?: { canvas: HTMLCanvasElement; alpha: boolean });
    setSize(width: number, height: number): void;
    render(scene: Scene, camera: PerspectiveCamera): void;
  }

  export class TorusKnotGeometry {
    constructor(radius: number, tube: number, tubularSegments: number, radialSegments: number);
  }

  export class MeshPhongMaterial {
    constructor(parameters: { color: number; shininess: number; wireframe: boolean });
  }

  export class Mesh {
    constructor(geometry: TorusKnotGeometry, material: MeshPhongMaterial);
    rotation: { x: number; y: number };
  }

  export class PointLight {
    constructor(color: number, intensity: number);
    position: { set: (x: number, y: number, z: number) => void };
  }
} 