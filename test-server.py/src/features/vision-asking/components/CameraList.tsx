import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { VisionCamera } from "../types";

interface CameraListProps {
  cameras: VisionCamera[];
  selectedCamera?: string;
  onCameraSelect: (cameraId: string) => void;
}

export const CameraList = ({ cameras, selectedCamera, onCameraSelect }: CameraListProps) => {
  return (
    <Card className="h-[calc(100vh-10rem)]">
      <CardHeader className="py-3">
        <CardTitle className="text-lg">Available Cameras</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[calc(100vh-14rem)]">
          <div className="grid grid-cols-1 gap-3 p-3">
            {cameras.map((camera) => (
              <button
                key={camera.id}
                onClick={() => onCameraSelect(camera.id)}
                className={`group w-full rounded-lg overflow-hidden transition-all hover:ring-2 hover:ring-primary/50 ${
                  selectedCamera === camera.id ? 'ring-2 ring-primary' : ''
                }`}
              >
                <div className="relative aspect-video w-full">
                  {/* Camera Feed/Thumbnail */}
                  <div className="absolute inset-0 bg-muted">
                    {camera.thumbnail ? (
                      <img 
                        src={camera.thumbnail} 
                        alt={camera.name} 
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-muted-foreground">
                        No Feed
                      </div>
                    )}
                  </div>
                  
                  {/* Gradient Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background/90" />
                  
                  {/* Camera Info */}
                  <div className="absolute bottom-0 left-0 right-0 p-2 flex items-end justify-between">
                    <span className="text-sm font-medium truncate">
                      {camera.name}
                    </span>
                    <span 
                      className={`text-xs px-1.5 py-0.5 rounded-full ${
                        camera.status === 'active' 
                          ? 'bg-green-500/20 text-green-500' 
                          : 'bg-red-500/20 text-red-500'
                      }`}
                    >
                      {camera.status}
                    </span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};