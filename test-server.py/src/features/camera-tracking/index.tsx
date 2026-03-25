import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Card, CardContent } from "@/components/ui/card";
import { CameraGrid } from './components/CameraGrid';
import { LayoutControls } from './components/LayoutControls';
import { CameraList } from './components/CameraList';
import { CameraOverview } from './components/CameraOverview';
import { FullscreenToolbar } from './components/FullscreenToolbar';
import { FullscreenChatbar } from './components/FullscreenChatbar';
import { GridSize, mockCameras } from './types';

const CameraTrackingPage = () => {
  const { t } = useTranslation();
  const [gridSize, setGridSize] = useState<GridSize>(4);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const cameraGridRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement && cameraGridRef.current) {
      cameraGridRef.current.requestFullscreen();
      setIsFullscreen(true);
    } else if (document.fullscreenElement) {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 mt-16">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 tracking-tight mb-4">{t('cameraTracking.title')}</h1>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-6">
        {/* Main content area with camera grid */}
        <div className="space-y-6">
          <Card ref={cameraGridRef}>
            <CardContent className="p-6">
              <CameraGrid
                cameras={mockCameras}
                gridSize={gridSize}
              />
              {isFullscreen && (
                <>
                  <FullscreenToolbar
                    gridSize={gridSize}
                    onGridSizeChange={setGridSize}
                    onExitFullscreen={() => toggleFullscreen()}
                  />
                  <FullscreenChatbar />
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right sidebar controls */}
        <div className="space-y-6">
          <LayoutControls
            gridSize={gridSize}
            onGridSizeChange={setGridSize}
            onToggleFullscreen={toggleFullscreen}
          />
          <CameraList cameras={mockCameras} />
        </div>
      </div>

      {/* Overview and Features sections */}
      <div className="mt-8">
        <CameraOverview />
      </div>
    </div>
  );
};

export default CameraTrackingPage;