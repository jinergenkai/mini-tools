import { useTranslation } from "react-i18next";
import {
  Type,
  Image,
  LineChart,
  Mic,
  Video,
  BarChart4
} from "@/components/modules/icon.module";
import { 
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle 
} from "@/components/modules/shadcn.module";
import { Link } from "react-router-dom";

type ServiceId = 
  | "camera-tracking"
  | "vision-asking"
  | "data-analytics"
  | "voice-recognition"
  | "video-processing"
  | "predictive-modeling";

const serviceIcons: Record<ServiceId, React.ComponentType<{ className?: string }>> = {
  "camera-tracking": Type,
  "vision-asking": Image,
  "data-analytics": LineChart,
  "voice-recognition": Mic,
  "video-processing": Video,
  "predictive-modeling": BarChart4
};

const serviceIds: ServiceId[] = [
  "camera-tracking",
  "vision-asking",
  "data-analytics",
  "voice-recognition",
  "video-processing",
  "predictive-modeling"
];

const Services = () => {
  const { t } = useTranslation();

  return (
    <section className="py-20 bg-white dark:bg-gray-900" id="services">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            {t('services.title')}
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            {t('services.subtitle')}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {serviceIds.map((serviceId) => {
            const Icon = serviceIcons[serviceId];
            return (
              <Link
                key={serviceId}
                to={
                  serviceId === "camera-tracking" ? "/ai-service/camera-tracking" :
                  serviceId === "vision-asking" ? "/ai-service/vision-asking" : "#"
                }
                className="block no-underline"
              >
                <Card
                  id={serviceId}
                  className="service-card-hover border-2 border-gray-100 dark:border-gray-800 transition-transform hover:scale-105"
                >
                  <CardHeader className="pb-2">
                    <div className="mb-2">
                      <Icon className="h-10 w-10 text-futureBlue" />
                    </div>
                    <CardTitle className="text-xl">
                      {t(`services.items.${serviceId}.title`)}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-base text-gray-600 dark:text-gray-400">
                      {t(`services.items.${serviceId}.description`)}
                    </CardDescription>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Services;