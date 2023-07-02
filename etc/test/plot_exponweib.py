import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import exponweib

alphas = [1.06, 1.06, 1.06]  # Shape parameter (a > 0)
cs = [1.0, 1.0, 1.0]  # Shape parameter (c > 0)
locs = [0.0, 0.0, 0.0]  # Location parameter (loc)
scales = [5.0, 10.0, 15.0]  # Scale parameter (scale > 0)

for i in range(len(locs)):
    loc = locs[i]
    scale = scales[i]
    a = alphas[i]
    c = cs[i]

    # Generate x values for the plot
    x = np.linspace(0, 10, 100)

    # Compute the corresponding y values using the normal distribution
    y = exponweib.pdf(x, a, c, loc=loc, scale=scale)

    # Create the plot
    legend_str = f"a: {a}; c: {c}; loc: {loc}; scale: {scale}"
    plt.plot(x, y, label=legend_str)

# Add labels and title
plt.xlabel("Days")
plt.ylabel("Probability Density")
plt.title("Exponweib Distribution")
plt.legend()

# Display the plot
plt.savefig("test.png")
plt.close()
