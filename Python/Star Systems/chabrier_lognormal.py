import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

# Chabrier simplification using a log-normal distribution
lognormal_num = np.random.lognormal(mean=0.2, sigma=0.69, size=10000)

# Filter masses between 0.08 and 120 (inclusive)
filtered_masses = lognormal_num[(lognormal_num >= 0.08) & (lognormal_num <= 1)]

# Fit a log-normal distribution to the data
shape, loc, scale = lognorm.fit(filtered_masses, floc=0)  # Fit log-normal distribution, fix loc to 0
x = np.linspace(0.08, 1, 200)  # Range for plotting the curve, with 200 points for smoothness
pdf = lognorm.pdf(x, shape, loc, scale)  # Probability density function

# Plot the smooth curve
plt.plot(x, pdf, 'b-', label=f'Fitted Log-Normal (σ={shape:.2f}, μ={np.log(scale):.2f})')

# Add labels and title
plt.xlabel('Mass (M☉)')
plt.ylabel('Probability Density')
plt.title('Chabrier IMF Masses (0.08-1 M☉) - Fitted Log-Normal Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()