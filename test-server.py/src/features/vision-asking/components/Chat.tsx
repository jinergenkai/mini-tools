import { useState, useEffect } from 'react';
import { Send, Mic, MicOff } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { ChatMessage } from '../types';

interface ChatProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
}

export const Chat = ({ messages, onSendMessage }: ChatProps) => {
  const { t, i18n } = useTranslation();
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);

  // Initialize or update speech recognition when language changes
  useEffect(() => {
    if (window.SpeechRecognition || window.webkitSpeechRecognition) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      // Configure recognition
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = i18n.language; // Set language from i18next
      
      recognitionInstance.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0].transcript)
          .join('');
        
        setMessage(transcript);
      };

      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
      };

      // Stop previous instance if exists
      if (recognition && isListening) {
        recognition.stop();
        setIsListening(false);
      }

      setRecognition(recognitionInstance);
    }
  }, [i18n.language]); // Re-initialize when language changes

  const toggleListening = () => {
    if (!recognition) {
      alert(t('errors.speechRecognitionNotSupported'));
      return;
    }

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    onSendMessage(message.trim());
    setMessage('');
  };

  return (
    <Card className="h-[calc(100vh-10rem)] flex flex-col">
      <CardHeader className="py-3 flex-shrink-0">
        <CardTitle className="text-lg">{t('vision.chat.title')}</CardTitle>
      </CardHeader>
      
      {/* Messages area */}
      <div className="flex-1 min-h-0">
        <ScrollArea className="h-full">
          <div className="flex flex-col gap-4 p-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${
                  msg.sender === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    msg.sender === 'user'
                      ? 'bg-primary text-primary-foreground shadow-sm'
                      : 'bg-muted text-foreground'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{msg.content}</p>
                  <time className={`text-[10px] mt-1 block ${
                    msg.sender === 'user'
                      ? 'text-primary-foreground/80'
                      : 'text-muted-foreground'
                  }`}>
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </time>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>
      
      {/* Enhanced input area */}
      <div className="flex-shrink-0 border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/75">
        <form onSubmit={handleSubmit} className="p-4">
          <div className="flex gap-2 items-start">
            <Button
              type="button"
              variant={isListening ? "destructive" : "outline"}
              size="icon"
              className={`h-[48px] w-[48px] rounded-xl shrink-0 ${
                isListening ? 'animate-pulse border-2 border-destructive' : 'hover:bg-muted'
              }`}
              onClick={toggleListening}
              title={isListening ? t('vision.chat.stopVoice') : t('vision.chat.startVoice')}
            >
              {isListening ? (
                <MicOff className="h-5 w-5" />
              ) : (
                <Mic className="h-5 w-5" />
              )}
            </Button>
            
            <Textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={t('vision.chat.inputPlaceholder')}
              className="min-h-[48px] resize-none rounded-xl bg-muted/30 border-muted-foreground/20 hover:border-primary/30 focus:border-primary focus:ring-1 focus:ring-primary"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              rows={1}
            />
            
            <Button
              type="submit"
              className="h-[48px] px-6 rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground transition-colors shrink-0"
              disabled={!message.trim()}
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>
          
          <div className="mt-2 text-xs text-muted-foreground px-2 flex justify-between">
            <span>{t('vision.chat.sendHint')}</span>
            {window.SpeechRecognition || window.webkitSpeechRecognition ? (
              <span>{t('vision.chat.voiceHint')}</span>
            ) : null}
          </div>
        </form>
      </div>
    </Card>
  );
};