import { useTranslation } from 'react-i18next';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { CameraFeed } from '../types';

interface CameraListProps {
  cameras: CameraFeed[];
}

export const CameraList = ({ cameras }: CameraListProps) => {
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('cameraTracking.controls.cameraList.title')}</CardTitle>
        <CardDescription>{t('cameraTracking.controls.cameraList.description')}</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[200px]">
          <div className="space-y-2">
            {cameras.map((camera) => (
              <div 
                key={camera.id} 
                className="flex items-center justify-between p-2 rounded-lg hover:bg-muted"
              >
                <span className="text-sm font-medium">{camera.name}</span>
                <span 
                  className={`text-xs ${
                    camera.status === 'active' ? 'text-green-500' : 'text-red-500'
                  }`}
                >
                  {camera.status}
                </span>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};