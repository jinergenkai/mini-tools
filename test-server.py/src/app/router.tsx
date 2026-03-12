import HomePage from "@/features/home-page";
import VisionAskingPage from "@/features/vision-asking";
import NotFoundPage from "@/features/not-found";
import CameraTrackingPage from "@/features/camera-tracking";
import ContactUs from "@/features/contact-us";
import MainLayout from "@/components/layout/MainLayout";
import { useRoutes, Navigate, Outlet } from "react-router-dom";

export function Router() {
    return useRoutes([
        {
            element: (
                <MainLayout>
                    <Outlet />
                </MainLayout>
            ),
            children: [
                { element: <HomePage />, index: true },
                { path: "contact", element: <ContactUs /> },
            ]
        },
        {
            element: (
                <MainLayout>
                    <Outlet />
                </MainLayout>
            ),
            path: "/ai-service",
            children: [
                { path: "camera-tracking", element: <CameraTrackingPage /> },
                { path: "vision-asking", element: <VisionAskingPage /> },
            ],
        },
        {
            path: "/404",
            element: <NotFoundPage />,
        },
        {
            path: "*",
            element: <Navigate to="/404" replace />,
        },
    ]);
}
