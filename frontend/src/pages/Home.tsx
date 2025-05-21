import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const features = [
  {
    title: 'Quantum Calculations',
    description: 'Perform complex quantum calculations with our advanced algorithms.',
    image: '/images/quantum.jpg',
  },
  {
    title: 'Real-time Analysis',
    description: 'Visualize results in real-time with interactive charts and graphs.',
    image: '/images/analysis.jpg',
  },
  {
    title: 'Batch Processing',
    description: 'Process multiple calculations simultaneously for efficient analysis.',
    image: '/images/batch.jpg',
  },
];

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 8,
          px: 2,
          textAlign: 'center',
          borderRadius: 2,
          mb: 4,
        }}
      >
        <Typography variant="h2" gutterBottom>
          Quantum Duality Theory
        </Typography>
        <Typography variant="h5" sx={{ mb: 4 }}>
          Explore the fascinating world of quantum mechanics through interactive calculations
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          size="large"
          onClick={() => navigate('/calculator')}
        >
          Get Started
        </Button>
      </Box>

      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Key Features
      </Typography>

      <Grid container spacing={4}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
            >
              <CardMedia
                component="img"
                height="200"
                image={feature.image}
                alt={feature.title}
              />
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom>
          Ready to Start?
        </Typography>
        <Typography variant="body1" sx={{ mb: 4 }}>
          Begin your quantum journey with our powerful calculator
        </Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={() => navigate('/calculator')}
        >
          Launch Calculator
        </Button>
      </Box>
    </Box>
  );
};

export default Home; 