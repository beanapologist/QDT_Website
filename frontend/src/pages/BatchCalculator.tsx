import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  TextField,
  Button,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import axios from 'axios';

interface BatchResult {
  id: string;
  value: number;
  result: number;
  status: 'success' | 'error';
  error?: string;
}

const BatchCalculator: React.FC = () => {
  const [values, setValues] = useState<string>('');
  const [type, setType] = useState<string>('currency');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [results, setResults] = useState<BatchResult[]>([]);

  const handleCalculate = async () => {
    try {
      setLoading(true);
      setError('');
      const valueArray = values
        .split(',')
        .map((v) => v.trim())
        .filter((v) => v)
        .map((v) => parseFloat(v));

      if (valueArray.length === 0) {
        throw new Error('Please enter at least one value');
      }

      const response = await axios.post('/api/batch-calculate', {
        values: valueArray,
        calculation_type: type,
      });

      setResults(response.data.results);
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Batch Calculator
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Input Parameters
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <TextField
                  label="Values (comma-separated)"
                  multiline
                  rows={4}
                  value={values}
                  onChange={(e) => setValues(e.target.value)}
                  placeholder="Enter values separated by commas (e.g., 1.5, 2.3, 3.7)"
                  fullWidth
                />
                <TextField
                  select
                  label="Calculation Type"
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                  fullWidth
                >
                  <option value="currency">Currency</option>
                  <option value="energy">Energy</option>
                  <option value="probability">Probability</option>
                </TextField>
                <Button
                  variant="contained"
                  onClick={handleCalculate}
                  disabled={loading || !values.trim()}
                  fullWidth
                >
                  {loading ? <CircularProgress size={24} /> : 'Calculate Batch'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Results
              </Typography>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              {results.length > 0 && (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Input Value</TableCell>
                        <TableCell>Result</TableCell>
                        <TableCell>Status</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.map((result) => (
                        <TableRow key={result.id}>
                          <TableCell>{result.value}</TableCell>
                          <TableCell>
                            {result.status === 'success'
                              ? result.result.toFixed(4)
                              : '-'}
                          </TableCell>
                          <TableCell>
                            {result.status === 'success' ? (
                              <Alert severity="success" sx={{ py: 0 }}>
                                Success
                              </Alert>
                            ) : (
                              <Alert severity="error" sx={{ py: 0 }}>
                                {result.error || 'Error'}
                              </Alert>
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BatchCalculator; 