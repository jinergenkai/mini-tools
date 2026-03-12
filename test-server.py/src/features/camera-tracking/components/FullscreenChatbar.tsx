import { useState } from 'react';
import { MessageCircle, X, ChevronDown, ChevronUp, Send } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

export const FullscreenChatbar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    // TODO: Implement chat functionality
    setMessage('');
  };

  if (isCollapsed) {
    return (
      <Button
        variant="ghost"
        size="icon"
        className="fixed left-4 bottom-20 bg-background/80 backdrop-blur-sm shadow-lg border rounded-full"
        onClick={() => setIsCollapsed(false)}
      >
        <MessageCircle className="h-4 w-4" />
      </Button>
    );
  }

  return (
    <Card className="fixed left-4 bottom-20 w-80 bg-background/80 backdrop-blur-sm shadow-lg">
      <div className="flex items-center justify-between p-3 border-b">
        <h3 className="text-sm font-medium">AI Assistant</h3>
        <div className="flex gap-1">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCollapsed(true)}
          >
            <ChevronDown className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <div className="h-60 overflow-y-auto p-3">
        {/* Chat messages will be displayed here */}
        <div className="text-sm text-muted-foreground">
          How can I help you with camera monitoring?
        </div>
      </div>
      <form onSubmit={handleSubmit} className="p-3 border-t">
        <div className="flex gap-2">
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="min-h-[40px] max-h-[120px]"
          />
          <Button type="submit" size="icon">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </Card>
  );
};