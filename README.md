# Quantum Duality Theory

A full-stack application exploring quantum mechanics and duality theory through interactive visualizations and calculations.

## Features

- Interactive 3D visualization of quantum phenomena
- Time crystal simulation and analysis
- Quantum gravity calculations
- Dark energy modeling
- Particle physics connections
- Hermetic principles integration
- Unity principles visualization

## Tech Stack

- Frontend: React with TypeScript
- Backend: Python/Flask
- Database: Redis for caching
- 3D Graphics: Three.js
- Styling: Tailwind CSS

## Prerequisites

- Node.js 16+
- Python 3.8+
- Redis

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd quantum-duality-theory
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Start Redis server:
```bash
redis-server
```

5. Start the development servers:

Backend:
```bash
python src/api/crystal_calculator_api.py
```

Frontend:
```bash
npm start
```

## Project Structure

```
.
├── src/
│   ├── api/              # Flask backend
│   ├── components/       # React components
│   ├── physics/         # Physics calculations
│   ├── services/        # Frontend services
│   ├── styles/          # CSS styles
│   └── types/           # TypeScript types
├── tests/               # Test files
├── public/              # Static assets
└── docs/               # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Quantum physics research community
- Three.js visualization library
- React and Flask frameworks

## Core Constants

- λ (Lambda) = 0.867: Coupling constant
- γ (Gamma) = 0.4497: Damping coefficient
- β (Beta) = 0.310: Fractal recursion
- η (Eta) = 0.520: Energy transfer rate
- φ (Phi) = 1.618033988749: Golden ratio

## Usage

### Python API

```python
from physics.crystal_calculator import CrystalCalculator

# Initialize calculator
calculator = CrystalCalculator()

# Calculate QDT value
result = calculator.calculate_crystal_enhanced_value(
    value=100.0,
    calculation_type='currency'
)

# Analyze convergence
analysis = calculator.analyze_convergence_path(result.time_series)
```

### Web Interface

1. Start the Flask server:
```bash
python src/api/crystal_calculator_api.py
```

2. Start the React development server:
```bash
cd frontend
npm install
npm start
```

3. Visit `http://localhost:3000` in your browser

## API Endpoints

### Calculate QDT Value
```http
POST /api/calculate
Content-Type: application/json

{
    "value": 100.0,
    "calculation_type": "currency",
    "evolution_steps": 100
}
```

### Analyze Convergence
```http
POST /api/analyze
Content-Type: application/json

{
    "time_series": {
        "void": [...],
        "filament": [...],
        "emergence": [...],
        "resonance": [...],
        "crystal_phase": [...],
        "convergence": [...]
    }
}
```

### Ask QDT Questions
```http
POST /api/ask
Content-Type: application/json

{
    "question": "What's the current convergence rate?"
}
```

## Rate Limits

- General: 100 requests per day, 10 per minute
- Calculations: 30 requests per minute
- Questions: 20 requests per minute

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black src/
flake8 src/
mypy src/
```

## Citation

If you use this software in your research, please cite:

```bibtex
@software{marin2024qdt,
    title = {Quantum Duality Theory Calculator},
    author = {Marin, Sarah},
    year = {2024},
    version = {1.0.0},
    url = {https://github.com/sarahmarin/quantum-duality-theory}
}
```

## Contact

Your Name - [@yourusername](https://twitter.com/yourusername)

Project Link: [https://github.com/yourusername/quantum-duality-theory](https://github.com/yourusername/quantum-duality-theory)

---

*Note: This theory is under active development. Contributions and feedback are welcome.*




