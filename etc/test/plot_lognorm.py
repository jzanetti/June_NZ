import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import lognorm

# Parameters for the normal distribution
locs = [0.0, 0.0]
scales = [5.0, 5.0]
shapes = [0.55, 0.1]


for i in range(len(locs)):
    loc = locs[i]
    scale = scales[i]
    s = shapes[i]

    # Generate x values for the plot
    x = np.linspace(loc - 3 * scale, loc + 3 * scale, 100)

    # Compute the corresponding y values using the normal distribution
    y = lognorm.pdf(x, loc=loc, scale=scale, s=s)

    # Create the plot
    legend_str = f"loc: {loc}; scale: {scale}; s: {s}"
    plt.plot(x, y, label=legend_str)

# Add labels and title
plt.xlabel("X")
plt.ylabel("Probability Density")
plt.title("Normal Distribution")
plt.legend()

# Display the plot
plt.savefig("test.png")
plt.close()
