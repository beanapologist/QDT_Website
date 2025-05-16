import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={
            <div className="App">
              <header className="App-header">
                <h1>Quantum Duality Theory</h1>
                <p>
                  Advanced Quantum Computing Research Platform
                </p>
              </header>
            </div>
          } />
          {/* Add more routes as needed */}
        </Routes>
      </Layout>
    </Router>
  );
}

export default App; 