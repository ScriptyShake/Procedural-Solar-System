import numpy as np
import matplotlib.pyplot as plt

# Define the power-law part of the Chabrier IMF for m >= 1 M_sun
def chabrier_imf_powerlaw(m):
    return 1.3 * m**(-2.3)

# Generate m values from 1 to 100 M_sun
m = np.linspace(1, 100, 1000)
# Compute corresponding p(m) values
p_m = chabrier_imf_powerlaw(m)

# Create the plot
plt.plot(m, p_m)
plt.xlabel('m (solar masses)')
plt.ylabel('p(m)')
plt.title('Power-law Part of the Chabrier IMF for m > 1 Solar Masses')
plt.grid(True)
plt.show()