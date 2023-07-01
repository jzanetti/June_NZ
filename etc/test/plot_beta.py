import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

# Parameters for the normal distribution
locs = [0.0, 0.0]
scales = [5.0, 5.0]


for i in range(len(locs)):
    loc = locs[i]
    scale = scales[i]

    # Generate x values for the plot
    x = np.linspace(loc - 3 * scale, loc + 3 * scale, 100)

    # Compute the corresponding y values using the normal distribution
    y = beta.pdf(x, loc=loc, scale=scale)

    # Create the plot
    legend_str = f"loc: {loc}; scale: {scale}"
    plt.plot(x, y, label=legend_str)

# Add labels and title
plt.xlabel("X")
plt.ylabel("Probability Density")
plt.title("Normal Distribution")
plt.legend()

# Display the plot
plt.savefig("test.png")
plt.close()