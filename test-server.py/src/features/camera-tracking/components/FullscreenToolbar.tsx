import { Grid2X2, Grid3X3, Layout, LayoutGrid, Minimize2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { GridSize } from '../types';

interface FullscreenToolbarProps {
  gridSize: GridSize;
  onGridSizeChange: (size: GridSize) => void;
  onExitFullscreen: () => void;
}

export const FullscreenToolbar = ({
  gridSize,
  onGridSizeChange,
  onExitFullscreen
}: FullscreenToolbarProps) => {
  return (
    <div className="fixed right-4 top-1/2 -translate-y-1/2 flex flex-col gap-2 bg-background/80 backdrop-blur-sm p-2 rounded-lg shadow-lg border">
      <Button 
        variant={gridSize === 1 ? "default" : "ghost"} 
        size="icon"
        onClick={() => onGridSizeChange(1)}
      >
        <Layout className="h-4 w-4" />
      </Button>
      <Button 
        variant={gridSize === 4 ? "default" : "ghost"} 
        size="icon"
        onClick={() => onGridSizeChange(4)}
      >
        <Grid2X2 className="h-4 w-4" />
      </Button>
      <Button 
        variant={gridSize === 9 ? "default" : "ghost"} 
        size="icon"
        onClick={() => onGridSizeChange(9)}
      >
        <Grid3X3 className="h-4 w-4" />
      </Button>
      <Button 
        variant={gridSize === 16 ? "default" : "ghost"} 
        size="icon"
        onClick={() => onGridSizeChange(16)}
      >
        <LayoutGrid className="h-4 w-4" />
      </Button>
      <div className="w-full h-px bg-border my-2" />
      <Button 
        variant="ghost"
        size="icon"
        onClick={onExitFullscreen}
      >
        <Minimize2 className="h-4 w-4" />
      </Button>
    </div>
  );
};