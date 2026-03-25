import { useTranslation } from 'react-i18next';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const CameraOverview = () => {
  const { t } = useTranslation();

  return (
    <div className="grid gap-6">
      <Card>
        <CardHeader>
          <CardTitle>{t('cameraTracking.overview.title')}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            {t('cameraTracking.overview.description')}
          </p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>{t('cameraTracking.features.title')}</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-2 text-muted-foreground">
            {(t('cameraTracking.features.list', { returnObjects: true }) as string[]).map((feature, index) => (
              <li key={index}>{feature}</li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};