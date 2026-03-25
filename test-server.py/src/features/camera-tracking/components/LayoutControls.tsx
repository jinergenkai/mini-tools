import { useTranslation } from 'react-i18next';
import { Grid2X2, Grid3X3, Layout, LayoutGrid, Maximize2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { GridSize } from '../types';

interface LayoutControlsProps {
  gridSize: GridSize;
  onGridSizeChange: (size: GridSize) => void;
  onToggleFullscreen: () => void;
}

export const LayoutControls = ({
  gridSize,
  onGridSizeChange,
  onToggleFullscreen
}: LayoutControlsProps) => {
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('cameraTracking.controls.layout.title')}</CardTitle>
        <CardDescription>{t('cameraTracking.controls.layout.description')}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-2 mb-2">
          <Button 
            variant={gridSize === 1 ? "default" : "outline"} 
            onClick={() => onGridSizeChange(1)}
            className="w-full"
          >
            <Layout className="h-4 w-4 mr-2" />
            1x1
          </Button>
          <Button 
            variant={gridSize === 4 ? "default" : "outline"} 
            onClick={() => onGridSizeChange(4)}
            className="w-full"
          >
            <Grid2X2 className="h-4 w-4 mr-2" />
            2x2
          </Button>
          <Button 
            variant={gridSize === 9 ? "default" : "outline"} 
            onClick={() => onGridSizeChange(9)}
            className="w-full"
          >
            <Grid3X3 className="h-4 w-4 mr-2" />
            3x3
          </Button>
          <Button 
            variant={gridSize === 16 ? "default" : "outline"} 
            onClick={() => onGridSizeChange(16)}
            className="w-full"
          >
            <LayoutGrid className="h-4 w-4 mr-2" />
            4x4
          </Button>
        </div>
        <Button 
          variant="outline"
          onClick={onToggleFullscreen}
          className="w-full flex items-center justify-center"
        >
          <Maximize2 className="h-4 w-4 mr-2" />
          {t('cameraTracking.controls.layout.fullscreen')}
        </Button>
      </CardContent>
    </Card>
  );
};