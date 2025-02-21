import random
import math
import matplotlib.pyplot as plt

# Constants (in SI and solar units)
M_SUN = 1.989e30  # kg
R_SUN = 6.96e8  # meters
L_SUN = 3.828e26  # watts
SIGMA = 5.6704e-8  # Stefan-Boltzmann constant (W/m^2/K^4)
T_SUN = 5778  # K (Sun's effective temperature)


def generate_star():
    # Step 1: Generate mass (in solar masses, M☉)
    mass = 10 ** random.uniform(math.log10(0.08), math.log10(20))

    # Step 2: Calculate luminosity (in solar luminosities, L☉)
    if mass < 0.43:
        luminosity = 0.23 * (mass ** 2.3)
    elif 0.43 <= mass <= 2:
        luminosity = mass ** 4
    else:
        luminosity = 1.4 * (mass ** 3.5)

    # Step 3: Calculate radius (in solar radii, R☉)
    if mass < 1:
        radius = mass ** 0.8
    else:
        radius = mass ** 0.6

    # Step 4: Calculate effective temperature (in Kelvin)
    l_si = luminosity * L_SUN
    r_si = radius * R_SUN
    temp_eff = (l_si / (4 * math.pi * (r_si ** 2) * SIGMA)) ** 0.25

    # Step 5: Calculate density (in kg/m^3)
    m_si = mass * M_SUN
    volume = (4 / 3) * math.pi * (r_si ** 3)
    density = m_si / volume

    # Step 6: Calculate lifetime (in years)
    lifetime = (mass / luminosity) * 1e10

    # Step 7: Determine spectral type and approximate RGB color
    if temp_eff > 30000:
        spectral_type = "O (Blue)"
        color = (0.5, 0.7, 1.0)  # Light blue
    elif 10000 <= temp_eff <= 30000:
        spectral_type = "B (Blue-White)"
        color = (0.8, 0.9, 1.0)  # Bluish-white
    elif 7500 <= temp_eff < 10000:
        spectral_type = "A (White)"
        color = (1.0, 1.0, 1.0)  # White
    elif 6000 <= temp_eff < 7500:
        spectral_type = "F (Yellow-White)"
        color = (1.0, 1.0, 0.9)  # Slightly yellowish white
    elif 5200 <= temp_eff < 6000:
        spectral_type = "G (Yellow)"
        color = (1.0, 0.95, 0.7)  # Yellow
    elif 3700 <= temp_eff < 5200:
        spectral_type = "K (Orange)"
        color = (1.0, 0.7, 0.4)  # Orange
    else:
        spectral_type = "M (Red)"
        color = (1.0, 0.4, 0.4)  # Reddish

    return {
        "Mass (M☉)": mass,
        "Luminosity (L☉)": luminosity,
        "Radius (R☉)": radius,
        "Temperature (K)": temp_eff,
        "Density (kg/m^3)": density,
        "Lifetime (years)": lifetime,
        "Spectral Type": spectral_type,
        "Color": color
    }


def plot_star_properties(star):
    # Normalize values for bar chart (relative to Sun or max reasonable value)
    properties = {
        "Mass": star["Mass (M☉)"] / 1,
        "Luminosity": star["Luminosity (L☉)"] / 1,
        "Radius": star["Radius (R☉)"] / 1,
        "Temperature": star["Temperature (K)"] / T_SUN,
        "Density": star["Density (kg/m^3)"] / 1410,  # Sun's avg density
        "Lifetime": star["Lifetime (years)"] / 1e10
    }

    # Bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(properties.keys(), properties.values(), color='skyblue')
    plt.title(f"Star Properties (Spectral Type: {star['Spectral Type']})")
    plt.ylabel("Normalized Value (relative to Sun)")
    plt.yscale('log')  # Log scale due to wide range
    plt.grid(True, which="both", ls="--", alpha=0.2)
    plt.show()

    # Color visualization
    plt.figure(figsize=(4, 4))
    plt.imshow([[star["Color"]]], extent=(0, 1, 0, 1))
    plt.title(f"Approximate Star Color ({star['Spectral Type']})")
    plt.axis('off')
    plt.show()

    # Print properties
    print("Generated Star Properties:")
    print(f"Mass: {star['Mass (M☉)']:.2f} M☉")
    print(f"Luminosity: {star['Luminosity (L☉)']:.2f} L☉")
    print(f"Radius: {star['Radius (R☉)']:.2f} R☉")
    print(f"Temperature: {star['Temperature (K)']:.0f} K")
    print(f"Density: {star['Density (kg/m^3)']:.0f} kg/m^3")
    print(f"Lifetime: {star['Lifetime (years)']:.2e} years")
    print(f"Spectral Type: {star['Spectral Type']}")


# Generate and visualize a star
star = generate_star()
plot_star_properties(star)