import numpy as np
from scipy.stats import norm, poisson
import matplotlib.pyplot as plt

# Constants
lambda_poisson = 3.05  # Poisson parameter for number of stars
m_min = 0.08   # Minimum mass (M_sun)
m_max = 150    # Maximum mass (M_sun)
a = np.log10(m_min)  # log10(0.08) ≈ -1.0969
b = 0          # log10(1), boundary between log-normal and power-law
x_max = np.log10(m_max)  # log10(150) ≈ 2.176
mu = a         # Mean of log-normal in log10 space
sigma = 0.69   # Standard deviation of log-normal
p_log = 0.891  # Approximate probability of m < 1 M_sun
age_universe = 13.8e9  # Age of the universe in years

# Function to sample stellar mass from Chabrier IMF
def sample_imf():
    while True:
        u = np.random.uniform(0, 1)
        if u < p_log:
            # Sample from log-normal (0.08 <= m < 1 M_sun)
            while True:
                x = np.random.normal(mu, sigma)
                if a <= x < b:  # x in [log10(0.08), 0)
                    break
        else:
            # Sample from power-law (m >= 1 M_sun)
            while True:
                v = np.random.uniform(0, 1)
                x = - (1 / 1.3) * np.log10(v)  # Power-law: p(x) ∝ 10^{-1.3 x}
                if x <= x_max:  # Ensure m <= 150 M_sun
                    break
        m = 10 ** x
        return m

# Function to generate a star system
def generate_system():
    # Sample number of stars (N >= 1)
    while True:
        N = poisson.rvs(lambda_poisson)
        if N >= 1:
            break
    if N == 1:
        # Single-star system
        m = sample_imf()
        return [m]
    else:
        # Multiple-star system
        m1 = sample_imf()  # Primary star mass
        masses = [m1]
        for _ in range(N - 1):
            q = np.random.uniform(0, 1)  # Mass ratio
            m = q * m1  # Companion mass
            masses.append(m)
        return masses

# Function to calculate main-sequence lifetime
def main_sequence_lifetime(m):
    return 1e10 * (m ** -2.5)  # in years

# Functions for main-sequence mass-luminosity and mass-temperature relationships
def ms_mass_to_luminosity(m):
    if m < 0.43:
        return 0.23 * m**2.3
    elif m < 2:
        return m**4
    elif m < 20:
        return 1.5 * m**3.5
    else:
        return 50000 * m

def ms_mass_to_temperature(m):
    if m < 0.43:
        return 3700 * (m / 0.43)**0.5
    elif m < 2:
        return 5772 * (m / 1)**0.5
    elif m < 20:
        return 5772 * (m / 1)**0.7
    else:
        return 40000

# Function to determine evolutionary stage and adjust L and T
def get_star_properties(m, age):
    tau_ms = main_sequence_lifetime(m)
    if age < tau_ms:
        # Main-sequence star
        L = ms_mass_to_luminosity(m)
        T = ms_mass_to_temperature(m)
        stage = 'MS'
    elif m < 0.5:
        # Low-mass stars: remain on MS for longer, but for simplicity, we'll assume they don't evolve significantly
        L = ms_mass_to_luminosity(m)
        T = ms_mass_to_temperature(m)
        stage = 'MS'
    elif 0.5 <= m < 8:
        if age < 1.1 * tau_ms:
            # Red giant
            L = 1000 * ms_mass_to_luminosity(m)
            T = 4000
            stage = 'RG'
        else:
            # White dwarf
            L = 0.001
            T = 10000
            stage = 'WD'
    else:
        # Supergiant
        L = 1e5 * ms_mass_to_luminosity(m)
        T = 10000
        stage = 'SG'
    return L, T, stage

# Generate 10,000 systems and collect all star properties
all_masses = []
all_luminosities = []
all_temperatures = []
all_stages = []

for _ in range(10000):
    system = generate_system()
    for m in system:
        age = np.random.uniform(0, age_universe)
        L, T, stage = get_star_properties(m, age)
        all_masses.append(m)
        all_luminosities.append(L)
        all_temperatures.append(T)
        all_stages.append(stage)

# Plot HR diagram with different colors for different stages
plt.figure(figsize=(10, 8))
colors = {'MS': 'blue', 'RG': 'red', 'SG': 'green', 'WD': 'purple'}
for stage in set(all_stages):
    idx = [i for i, s in enumerate(all_stages) if s == stage]
    plt.scatter([all_temperatures[i] for i in idx], [all_luminosities[i] for i in idx],
                s=1, color=colors[stage], alpha=0.5, label=stage)

plt.xscale('log')
plt.yscale('log')
plt.gca().invert_xaxis()  # Hotter stars on the left
plt.xlabel('Effective Temperature (K)')
plt.ylabel('Luminosity (L_sun)')
plt.title('Hertzsprung-Russell Diagram with Evolved Stars')
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.show()