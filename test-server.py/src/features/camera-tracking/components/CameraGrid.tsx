import { Card } from "@/components/ui/card";
import { CameraFeed, GridSize, gridConfigs } from "../types";

interface CameraGridProps {
  cameras: CameraFeed[];
  gridSize: GridSize;
}

export const CameraGrid = ({ cameras, gridSize }: CameraGridProps) => {
  return (
    <div className={`grid ${gridConfigs[gridSize]} gap-4`}>
      {cameras.slice(0, gridSize).map((camera) => (
        <Card key={camera.id} className="relative aspect-video bg-muted overflow-hidden">
          {
            camera.id === 1 ? (
              <img
                src="http://localhost:5000/video_feed"
                alt={camera.name}
                className="absolute inset-0 w-full h-full object-cover"
              />
            ) :
              (
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm text-muted-foreground">{camera.name}</span>
                </div>
              )
          }
          <div className="absolute bottom-2 left-2 bg-black/50 px-2 py-1 rounded">
            <span className="text-sm text-white">{camera.name}</span>
          </div>
        </Card>
      ))}
    </div>
  );
};