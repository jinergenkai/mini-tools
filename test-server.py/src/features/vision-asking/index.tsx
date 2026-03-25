import { useState } from "react";
import { useTranslation } from "react-i18next";
import { CameraList } from "./components/CameraList";
import { Chat } from "./components/Chat";
import { VisionCamera, ChatMessage } from "./types";

// Mock data for demonstration
const mockCameras: VisionCamera[] = [
  { id: "1", name: "Front Door", status: "active", thumbnail: "/placeholder.svg" },
  { id: "2", name: "Back Yard", status: "active", thumbnail: "/placeholder.svg" },
  { id: "3", name: "Garage", status: "inactive" },
  { id: "4", name: "Living Room", status: "active", thumbnail: "/placeholder.svg" },
];

const initialMessages: ChatMessage[] = [
  {
    id: "1",
    content: "Hello! I can help you analyze what's happening in your camera feeds. Select a camera to get started.",
    sender: "ai",
    timestamp: new Date(),
  },
];

const VisionAskingPage = () => {
  const { t } = useTranslation();
  const [selectedCamera, setSelectedCamera] = useState<string>();
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);

  const handleCameraSelect = (cameraId: string) => {
    setSelectedCamera(cameraId);
    const camera = mockCameras.find((c) => c.id === cameraId);
    if (camera) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          content: `Now monitoring ${camera.name}. What would you like to know about this camera feed?`,
          sender: "ai",
          timestamp: new Date(),
        },
      ]);
    }
  };

  const handleSendMessage = (content: string) => {
    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString(),
        content,
        sender: "user",
        timestamp: new Date(),
      },
    ]);

    // Simulate AI response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          content: "I'm analyzing the camera feed. This is a mock response - actual AI vision analysis would be implemented here.",
          sender: "ai",
          timestamp: new Date(),
        },
      ]);
    }, 1000);
  };

  return (
    <div className="container mx-auto p-4 mt-16">
      <h1 className="text-3xl font-bold mb-6">
        {t('header.services.vision-asking')}
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-[350px_1fr] gap-4">
        <div>
          <CameraList
            cameras={mockCameras}
            selectedCamera={selectedCamera}
            onCameraSelect={handleCameraSelect}
          />
        </div>
        <div>
          <Chat
            messages={messages}
            onSendMessage={handleSendMessage}
          />
        </div>
      </div>
    </div>
  );
};

export default VisionAskingPage;