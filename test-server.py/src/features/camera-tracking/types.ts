export type GridSize = 1 | 4 | 9 | 16;

export interface CameraFeed {
  id: number;
  name: string;
  status: 'active' | 'inactive';
}

export const gridConfigs = {
  1: 'grid-cols-1',
  4: 'grid-cols-2',
  9: 'grid-cols-3',
  16: 'grid-cols-4'
} as const;

// Mock data
export const mockCameras: CameraFeed[] = Array.from({ length: 16 }, (_, i) => ({
  id: i + 1,
  name: `Camera ${i + 1}`,
  status: 'active'
}));