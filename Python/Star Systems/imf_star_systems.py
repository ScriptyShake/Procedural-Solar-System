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

# Generate 10,000 systems and collect all star masses
all_masses = []
for _ in range(10000):
    system = generate_system()
    all_masses.extend(system)

# Plot histogram of log10(m)
plt.figure(figsize=(8, 6))
log_masses = np.log10(all_masses)
plt.hist(log_masses, bins=50, density=True, color='skyblue', edgecolor='black')
plt.xlabel(r'$\log_{10}(m / M_\odot)$')
plt.ylabel('Probability Density')
plt.title('Distribution of Star Masses')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# Print five example systems
print("\nExample Star Systems:")
for i in range(5):
    system = generate_system()
    masses_rounded = [round(m, 3) for m in system]
    print(f"System {i+1}: {len(system)} stars, masses (M_sun): {masses_rounded}")