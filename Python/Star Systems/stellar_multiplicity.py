import numpy as np
import matplotlib.pyplot as plt

# Chabrier simplification using a log-normal distribution
lognormal_num = np.random.lognormal(mean=0.2, sigma=0.69, size=10000)

# Filter masses between 0.08 and 120 (inclusive)
filtered_masses = lognormal_num[(lognormal_num >= 0.08) & (lognormal_num <= 120)]

# Print the filtered masses
print("Filtered masses (0.08 to 120):")
print(filtered_masses)
print(f"Number of masses retained: {len(filtered_masses)}")

# Histogram of filtered masses
plt.hist(filtered_masses, bins=30)
plt.xlabel('Mass (M_\u2609)')  # M_\u2609 is the solar mass symbol
plt.ylabel('Frequency')
plt.title('Chabrier IMF Masses (0.08–120 M_\u2609)')
plt.show()