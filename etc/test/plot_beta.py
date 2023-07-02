import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

# Parameters for the normal distribution
locs = [0.0, 0.0, 0.0]
scales = [2.0, 5.0, 8.0]
alphas = [2.29, 2.29, 2.29]
betas = [19.05, 19.05, 19.05]

for i in range(len(locs)):
    loc = locs[i]
    scale = scales[i]
    a = alphas[i]
    b = betas[i]

    # Generate x values for the plot
    x = np.linspace(0, 10, 100)

    # Compute the corresponding y values using the normal distribution
    y = beta.pdf(x, a, b, loc=loc, scale=scale)

    # Create the plot
    legend_str = f"a: {a}; b: {b}; loc: {loc}; scale: {scale}"
    plt.plot(x, y, label=legend_str)

# Add labels and title
plt.xlabel("Days")
plt.ylabel("Probability Density")
plt.title("Beta Distribution")
plt.legend()

# Display the plot
plt.savefig("test.png", bbox_inches="tight")
plt.close()
