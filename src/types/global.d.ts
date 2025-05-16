/// <reference types="react" />
/// <reference types="next" />

declare module 'framer-motion' {
  import { ComponentType, ReactElement } from 'react';

  export interface MotionProps {
    initial?: any;
    animate?: any;
    transition?: any;
    className?: string;
    scale?: number;
  }

  export const motion: {
    [K in keyof JSX.IntrinsicElements]: ComponentType<JSX.IntrinsicElements[K] & MotionProps>;
  };
}

declare module 'react-latex' {
  const Latex: React.FC<{ children: string }>;
  export default Latex;
}

declare module 'react-chartjs-2' {
  import { ChartData, ChartOptions } from 'chart.js';
  
  interface LineProps {
    data: ChartData;
    options?: ChartOptions;
  }
  
  export const Line: React.FC<LineProps>;
}

declare module '*.css' {
  const content: { [className: string]: string };
  export default content;
}

declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: any;
  }
}

declare module '*.svg' {
  const content: React.FC<React.SVGProps<SVGSVGElement>>;
  export default content;
}

declare module '*.png' {
  const content: string;
  export default content;
}

declare module '*.jpg' {
  const content: string;
  export default content;
} 