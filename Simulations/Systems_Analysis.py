import numpy as np
from typing import Dict

class QDTEnergyAnalyzer:
    def __init__(self):
        # Core QDT Constants
        self.LAMBDA = 0.867    # Coupling constant
        self.GAMMA = 0.4497    # Damping coefficient
        self.BETA = 0.310      # Fractal recursion strength
        self.ETA = 0.520       # Energy transfer rate
        self.PHI = 1.6180      # Golden Ratio
        self.CMB_COUPLING = 3.67e-5  # CMB coupling constant

        # Physical Constants
        self.G = 6.674e-11     # Gravitational constant (Nm²/kg²)
        self.c = 2.998e8       # Speed of light (m/s)
        self.h = 6.626e-34     # Planck constant (Js)

    def calculate_energies(self, mass: float, radius: float, spin: float) -> Dict:
        """
        Calculate energy components for a system based on QDT.

        Args:
            mass: Mass in solar masses
            radius: Radius in meters
            spin: Spin (dimensionless)

        Returns:
            A dictionary containing energy components and derived parameters.
        """
        # Convert mass to kilograms
        M = mass * 2e30  # Solar masses to kg
        r = radius

        # Characteristic Scales
        r_s = 2 * self.G * M / self.c**2  # Schwarzschild radius
        xi = r * self.c**2 / (self.G * M)  # Scale parameter

        # Cosmic Energy
        E_cosmic = self.LAMBDA * (self.G * M / r) * np.exp(-self.GAMMA * (r / r_s))

        # Quantum Energy
        psi = np.exp(-self.GAMMA * r / (2 * r_s))  # Wave function
        E_quantum = (self.h * self.c / (r * self.BETA)) * abs(psi)**2

        # Emergence Energy
        phase = 0.5 * (1 + np.tanh(self.ETA * self.BETA * spin * (r / r_s)))
        E_emergence = self.LAMBDA * E_cosmic * phase * np.exp(-self.BETA * xi)

        # Total Energy
        E_total = E_cosmic + E_quantum + E_emergence

        # Energy Ratios
        ratios = {
            "quantum_cosmic": E_quantum / E_cosmic if E_cosmic != 0 else 0,
            "emergence_cosmic": E_emergence / E_cosmic if E_cosmic != 0 else 0
        }

        return {
            "energies": {
                "cosmic": E_cosmic,
                "quantum": E_quantum,
                "emergence": E_emergence,
                "total": E_total
            },
            "ratios": ratios,
            "parameters": {
                "schwarzschild_radius": r_s,
                "scale_parameter": xi
            }
        }

    def analyze_system(self, name: str, mass: float, radius: float, spin: float) -> Dict:
        """
        Perform a full analysis for a given system.

        Args:
            name: System name
            mass: Mass in solar masses
            radius: Radius in meters
            spin: Spin (dimensionless)

        Returns:
            A dictionary containing the analysis results.
        """
        results = self.calculate_energies(mass, radius, spin)

        # Conservation Error
        component_sum = (results["energies"]["cosmic"] +
                         results["energies"]["quantum"] +
                         results["energies"]["emergence"])
        conservation_error = abs(results["energies"]["total"] - component_sum) / component_sum

        # Hierarchy Check
        hierarchy = {
            "cosmic_dominated": results["energies"]["cosmic"] > results["energies"]["emergence"],
            "quantum_suppressed": results["energies"]["quantum"] < results["energies"]["cosmic"],
            "emergence_bounded": results["energies"]["emergence"] < results["energies"]["cosmic"] * 10
        }

        return {
            "system": name,
            "energies": results["energies"],
            "ratios": results["ratios"],
            "conservation_error": conservation_error,
            "hierarchy": hierarchy,
            "parameters": results["parameters"]
        }

    def analyze_all_systems(self) -> Dict:
        """
        Analyze a set of predefined systems.

        Returns:
            A dictionary containing the analysis results for all systems.
        """
        systems = {
            "GRS_1915+105": (12.4, 36.8e3, 0.98),
            "M87": (6.5e9, 1.9e13, 0.90),
            "XTE_J1550-564": (9.1, 27.0e3, 0.95)
        }
        return {name: self.analyze_system(name, *params) for name, params in systems.items()}

# Example Execution
if __name__ == "__main__":
    qdt_analyzer = QDTEnergyAnalyzer()
    results = qdt_analyzer.analyze_all_systems()

    # Print Results
    for system, result in results.items():
        print(f"\nSystem: {system}")
        print("Energy Components:")
        for key, value in result["energies"].items():
            print(f"  {key}: {value:.2e} J")
        print("Energy Ratios:")
        for key, value in result["ratios"].items():
            print(f"  {key}: {value:.2e}")
        print("Hierarchy Check:")
        for key, status in result["hierarchy"].items():
            print(f"  {key}: {'✓' if status else '✗'}")