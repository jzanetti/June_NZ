import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma

# Parameters for the normal distribution
shapes = [1.0, 1.0, 3.0]
scales = [1.0, 1.5, 1.0]
shifts = [6.785695005231625, 6.785695005231625, 6.785695005231625]


for i in range(len(shapes)):
    shape = shapes[i]
    scale = scales[i]
    shift = shifts[i]

    # Generate x values for the plot
    x = np.linspace(0, 10, 100)

    # Compute the corresponding y values using the normal distribution
    y = gamma.pdf(x, a=shape, loc=shift, scale=scale)

    # gamma_pdf(
    #        x=time_from_infection, a=self.shape, loc=self.shift, scale=self.scale
    #    )
    # Create the plot
    legend_str = f"shape: {shape}; scale: {scale}"
    plt.plot(x, y, label=legend_str)

# Add labels and title
plt.xlabel("X")
plt.ylabel("Probability Density")
plt.title("Gamma Distribution")
plt.legend()

# Display the plot
plt.savefig("test.png")
plt.close()
