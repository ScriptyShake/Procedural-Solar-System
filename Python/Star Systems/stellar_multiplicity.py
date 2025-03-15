import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------
#           GENERATE M⊙primary FOLLOWING AN IMF
#--------------------------------------------------------

# -------------- Log Normal Piece
lognormal_mass = np.random.lognormal(mean=0.2, sigma=0.69, size=10000)
filtered_lognormal_mass = lognormal_mass[(lognormal_mass >= 0.08) & (lognormal_mass <= 1)]

# -------------- Power Law Piece
def chabrier_imf_powerlaw(m):
    return 1.3 * m**(-2.3)

# sample masses according to the IMF
def sample_imf(n_samples, m_min=1.01, m_max=120):
    m_grid = np.linspace(m_min, m_max, 1000)
    pdf = chabrier_imf_powerlaw(m_grid)
    cdf = np.cumsum(pdf)
    cdf /= cdf[-1]
    u = np.random.uniform(0, 1, n_samples)
    return np.interp(u, cdf, m_grid)

m = sample_imf(10000)

# -------------- Convert to Python list
mass_list_lognormal = filtered_lognormal_mass.tolist()
mass_list_powerlaw = m.tolist()
primary_masses = mass_list_lognormal + mass_list_powerlaw  # full list of primary star masses

#--------------------------------------------------------
#               DEDUCE STELLAR MULTIPLICITY
#--------------------------------------------------------

# -------------- Multiplicity Properties table by Gaspard Duchêne and Adam Kraus (simplified)

def find_mf(m):
    if m < 0.1:
        return 0.22
    elif 0.1 <= m <= 0.5:
        return 0.26
    elif 0.5 < m <= 1.3:
        return 0.44
    elif 1.3 < m <= 5:
        return 0.50
    elif 5 < m <= 16:
        return 0.60
    elif m > 16:
        return 0.80

# -------------- Find if star-system is single or multiple based on M⊙primary
for i in range(len(primary_masses)):
    mass = primary_masses[i]
    mf = find_mf(mass)
    random_number = np.random.uniform(0, 1)
    if random_number <= mf:
        ...
        # do logic for single
    else:
        ...
        # do logic for multiple








# -------------- Data Visualization & Validation
plt.figure(figsize=(10, 6))
plt.hist(primary_masses, bins=50, color='skyblue', alpha=0.7, edgecolor='black', label='Primary Masses')

plt.xlabel('Mass (M☉)')
plt.ylabel('Frequency')
plt.title('Histogram of Primary Star Masses')
plt.grid(True, alpha=0.3)
plt.legend()

plt.show()

random_masses = np.random.choice(primary_masses, 20, replace=False)
print("20 Random Masses from primary_masses:", random_masses)

masses_above_10 = sum(mass > 10 for mass in primary_masses)
print("Number of masses above 10:", masses_above_10)

masses_above_5 = sum(mass > 5 for mass in primary_masses)
percentage_above_5 = (masses_above_5 / len(primary_masses)) * 100
print(f"Percentage of masses above 5: {percentage_above_5:.2f}%")
