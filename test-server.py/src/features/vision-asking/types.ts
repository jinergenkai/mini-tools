export interface VisionCamera {
  id: string;
  name: string;
  status: 'active' | 'inactive';
  thumbnail?: string;
}

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}