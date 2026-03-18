"""
Test runner for Monte Carlo simulation
"""
import pandas as pd
from simulate_monte_carlo import run_monte_carlo_simulation
from generate_html import save_html

# Load data
print("Loading tournament data...")
kenpom_data = pd.read_csv('kenpom_tournament_data.csv')
torvik_data = pd.read_csv('torvik_tournament_data.csv')

print(f"Loaded {len(kenpom_data)} teams from Kenpom")
print(f"Loaded {len(torvik_data)} teams from Torvik")

# Run Monte Carlo simulation
probabilities = run_monte_carlo_simulation(kenpom_data, torvik_data, n_sims=10000)

print("\n Simulation complete!")

# Generate HTML output
save_html(probabilities, filename='monte_carlo_results.html', n_sims=10000)

print("\n" + "="*70)
print("All outputs generated successfully!")
print("Terminal output with all teams")
print("monte_carlo_results.html (open in browser)")
print("="*70)