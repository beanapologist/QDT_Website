import React, { useState, useCallback, useMemo } from 'react';
import { 
  Container, 
  Paper, 
  Typography, 
  TextField, 
  Button, 
  Grid,
  Box,
  CircularProgress,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tooltip
} from '@mui/material';
import QDTVisualizer from '../components/QDTVisualizer';

interface CalculationResult {
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
  time_series: {
    void_energy: number[];
    filament_energy: number[];
    emergence_energy: number[];
    crystal_phase: number[];
    resonance: number[];
    steps: number[];
  };
}

const calculationTypes = [
  { value: 'currency', label: 'Currency', description: 'Calculate quantum duality for monetary values' },
  { value: 'energy', label: 'Energy', description: 'Calculate quantum duality for energy measurements' },
  { value: 'probability', label: 'Probability', description: 'Calculate quantum duality for probability distributions' }
];

const Calculator: React.FC = () => {
  const [value, setValue] = useState<string>('');
  const [calculationType, setCalculationType] = useState<string>('currency');
  const [evolutionSteps, setEvolutionSteps] = useState<string>('100');
  const [result, setResult] = useState<CalculationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleCalculate = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:5001/api/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          value: parseFloat(value),
          calculation_type: calculationType,
          evolution_steps: parseInt(evolutionSteps)
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to calculate');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [value, calculationType, evolutionSteps]);

  const isFormValid = useMemo(() => {
    const numValue = parseFloat(value);
    const numSteps = parseInt(evolutionSteps);
    return !isNaN(numValue) && 
           !isNaN(numSteps) && 
           numSteps >= 10 && 
           numSteps <= 1000;
  }, [value, evolutionSteps]);

  const handleKeyPress = useCallback((event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && isFormValid) {
      handleCalculate();
    }
  }, [handleCalculate, isFormValid]);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Quantum Duality Calculator
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Value"
              type="number"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyPress={handleKeyPress}
              margin="normal"
              error={value !== '' && isNaN(parseFloat(value))}
              helperText={value !== '' && isNaN(parseFloat(value)) ? 'Please enter a valid number' : ''}
            />
          </Grid>
          
          <Grid item xs={12} md={4}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Calculation Type</InputLabel>
              <Select
                value={calculationType}
                onChange={(e) => setCalculationType(e.target.value)}
                label="Calculation Type"
              >
                {calculationTypes.map((type) => (
                  <MenuItem key={type.value} value={type.value}>
                    <Tooltip title={type.description} placement="right">
                      <span>{type.label}</span>
                    </Tooltip>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Evolution Steps"
              type="number"
              value={evolutionSteps}
              onChange={(e) => setEvolutionSteps(e.target.value)}
              onKeyPress={handleKeyPress}
              margin="normal"
              inputProps={{ min: 10, max: 1000 }}
              error={evolutionSteps !== '' && (parseInt(evolutionSteps) < 10 || parseInt(evolutionSteps) > 1000)}
              helperText={evolutionSteps !== '' && (parseInt(evolutionSteps) < 10 || parseInt(evolutionSteps) > 1000) 
                ? 'Steps must be between 10 and 1000' 
                : ''}
            />
          </Grid>
        </Grid>

        <Box sx={{ mt: 3, mb: 3 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleCalculate}
            disabled={loading || !isFormValid}
            fullWidth
            size="large"
          >
            {loading ? <CircularProgress size={24} /> : 'Calculate'}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Box sx={{ mt: 4 }}>
            <QDTVisualizer
              calculationResult={result}
              timeSeries={result.time_series}
            />
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default React.memo(Calculator); 