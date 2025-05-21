import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  CircularProgress,
  Alert,
  Paper,
  Avatar,
} from '@mui/material';
import { Send as SendIcon, SmartToy as BotIcon, Person as UserIcon } from '@mui/icons-material';
import axios from 'axios';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const QA: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/qa', {
        question: userMessage.content,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.answer,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.response?.data?.error || 'An error occurred while getting the response');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Quantum Duality Q&A
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="body1" color="text.secondary">
            Ask questions about quantum duality theory, calculations, or any related topics.
            Our AI assistant will help you understand the concepts better.
          </Typography>
        </CardContent>
      </Card>

      <Box sx={{ height: 'calc(100vh - 300px)', display: 'flex', flexDirection: 'column' }}>
        <Paper
          elevation={3}
          sx={{
            flex: 1,
            mb: 2,
            p: 2,
            overflow: 'auto',
            backgroundColor: 'background.paper',
          }}
        >
          {messages.map((message) => (
            <Box
              key={message.id}
              sx={{
                display: 'flex',
                justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                mb: 2,
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                  alignItems: 'flex-start',
                  maxWidth: '70%',
                }}
              >
                <Avatar
                  sx={{
                    bgcolor: message.role === 'user' ? 'primary.main' : 'secondary.main',
                    ml: message.role === 'user' ? 2 : 0,
                    mr: message.role === 'user' ? 0 : 2,
                  }}
                >
                  {message.role === 'user' ? <UserIcon /> : <BotIcon />}
                </Avatar>
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    backgroundColor: message.role === 'user' ? 'primary.dark' : 'background.paper',
                    color: message.role === 'user' ? 'white' : 'text.primary',
                    borderRadius: 2,
                  }}
                >
                  <Typography variant="body1">{message.content}</Typography>
                  <Typography
                    variant="caption"
                    sx={{
                      display: 'block',
                      mt: 1,
                      color: message.role === 'user' ? 'rgba(255, 255, 255, 0.7)' : 'text.secondary',
                    }}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </Typography>
                </Paper>
              </Box>
            </Box>
          ))}
          <div ref={messagesEndRef} />
        </Paper>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Paper
          component="form"
          onSubmit={handleSubmit}
          sx={{
            p: 2,
            display: 'flex',
            gap: 2,
            backgroundColor: 'background.paper',
          }}
        >
          <TextField
            fullWidth
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about quantum duality..."
            disabled={loading}
            multiline
            maxRows={4}
          />
          <Button
            type="submit"
            variant="contained"
            disabled={loading || !input.trim()}
            sx={{ minWidth: 100 }}
          >
            {loading ? <CircularProgress size={24} /> : <SendIcon />}
          </Button>
        </Paper>
      </Box>
    </Box>
  );
};

export default QA; 