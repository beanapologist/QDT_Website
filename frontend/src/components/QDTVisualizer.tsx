import React, { useMemo } from 'react';
import { Box, Grid, Paper, Typography } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface QDTVisualizerProps {
  calculationResult: {
    void_energy: number;
    filament_energy: number;
    emergence_energy: number;
    crystal_phase: number;
    resonance: number;
    convergence_metrics: {
      stability_score: number;
      phase_coherence: number;
      convergence_rate: number;
    };
  };
  timeSeries: {
    void_energy: number[];
    filament_energy: number[];
    emergence_energy: number[];
    crystal_phase: number[];
    resonance: number[];
    steps: number[];
  };
}

const QDTVisualizer: React.FC<QDTVisualizerProps> = ({ calculationResult, timeSeries }) => {
  // Memoize chart options to prevent unnecessary re-renders
  const chartOptions: ChartOptions<'line'> = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 750,
      easing: 'easeInOutQuart'
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    },
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          usePointStyle: true,
          padding: 20
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        titleColor: '#000',
        bodyColor: '#666',
        borderColor: '#ddd',
        borderWidth: 1,
        padding: 10,
        displayColors: true,
        callbacks: {
          label: (context) => {
            const value = context.parsed.y;
            return `${context.dataset.label}: ${(value * 100).toFixed(1)}%`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => `${(Number(value) * 100).toFixed(0)}%`
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    }
  }), []);

  // Memoize chart data to prevent unnecessary re-renders
  const energyDistributionData = useMemo(() => ({
    labels: ['Void Energy', 'Filament Energy', 'Emergence Energy'],
    datasets: [{
      label: 'Energy Distribution',
      data: [
        calculationResult.void_energy,
        calculationResult.filament_energy,
        calculationResult.emergence_energy,
      ],
      backgroundColor: [
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
      ],
      borderColor: [
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)',
      ],
      borderWidth: 1,
    }],
  }), [calculationResult]);

  const timeEvolutionData = useMemo(() => ({
    labels: timeSeries.steps,
    datasets: [
      {
        label: 'Void Energy',
        data: timeSeries.void_energy,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 2
      },
      {
        label: 'Filament Energy',
        data: timeSeries.filament_energy,
        borderColor: 'rgb(153, 102, 255)',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 2
      },
      {
        label: 'Emergence Energy',
        data: timeSeries.emergence_energy,
        borderColor: 'rgb(255, 159, 64)',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 2
      },
    ],
  }), [timeSeries]);

  const resonanceData = useMemo(() => ({
    labels: timeSeries.steps,
    datasets: [
      {
        label: 'Crystal Phase',
        data: timeSeries.crystal_phase,
        borderColor: 'rgb(54, 162, 235)',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 2
      },
      {
        label: 'Resonance',
        data: timeSeries.resonance,
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 2
      },
    ],
  }), [timeSeries]);

  // Memoize metrics display to prevent unnecessary re-renders
  const metrics = useMemo(() => ({
    stability: (calculationResult.convergence_metrics.stability_score * 100).toFixed(1),
    coherence: (calculationResult.convergence_metrics.phase_coherence * 100).toFixed(1),
    convergence: (calculationResult.convergence_metrics.convergence_rate * 100).toFixed(1),
    resonance: (calculationResult.resonance * 100).toFixed(1)
  }), [calculationResult]);

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '300px' }}>
            <Typography variant="h6" gutterBottom>
              Energy Distribution
            </Typography>
            <Line options={chartOptions} data={energyDistributionData} />
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '300px' }}>
            <Typography variant="h6" gutterBottom>
              Time Evolution
            </Typography>
            <Line options={chartOptions} data={timeEvolutionData} />
          </Paper>
        </Grid>
        
        <Grid item xs={12}>
          <Paper sx={{ p: 2, height: '300px' }}>
            <Typography variant="h6" gutterBottom>
              Resonance & Crystal Phase
            </Typography>
            <Line options={chartOptions} data={resonanceData} />
          </Paper>
        </Grid>
        
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              System Metrics
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="subtitle1">Stability Score</Typography>
                <Typography variant="h6">{metrics.stability}%</Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="subtitle1">Phase Coherence</Typography>
                <Typography variant="h6">{metrics.coherence}%</Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="subtitle1">Convergence Rate</Typography>
                <Typography variant="h6">{metrics.convergence}%</Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="subtitle1">Final Resonance</Typography>
                <Typography variant="h6">{metrics.resonance}%</Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default React.memo(QDTVisualizer); 