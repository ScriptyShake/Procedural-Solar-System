import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Define the Chabrier IMF power-law function
def chabrier_imf_powerlaw(m):
    return 1.3 * m**(-2.3)

# Function to sample masses according to the IMF
def sample_imf(n_samples, m_min=1.01, m_max=120):
    m_grid = np.linspace(m_min, m_max, 1000)
    pdf = chabrier_imf_powerlaw(m_grid)
    cdf = np.cumsum(pdf)
    cdf /= cdf[-1]
    u = np.random.uniform(0, 1, n_samples)
    return np.interp(u, cdf, m_grid)

# Generate 10,000 masses following the Chabrier IMF
m = sample_imf(10000)

# Print 20 masses from the generated set
print("20 masses following Chabrier IMF (in solar masses):")
print(m[:20])

# Create the curved graph
plt.figure(figsize=(10, 6))

# Plot histogram of the sampled masses
plt.hist(m, bins=50, density=True, alpha=0.5, color='skyblue', label='Histogram of Samples')

# Add a smooth density curve using kernel density estimation
kde = gaussian_kde(m)
x = np.linspace(1.01, 120, 1000)  # Smooth range for the curve
plt.plot(x, kde(x), 'r-', lw=2, label='Density Curve')

# Customize the plot
plt.xlabel('Mass (solar masses)')
plt.ylabel('Density')
plt.title('Chabrier IMF Power-law Distribution (m > 1 Solar Mass)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xscale('log')  # Log scale for x-axis to see the full range
plt.show()