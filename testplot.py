import numpy as np
import mpld3
import matplotlib.pyplot as plt

from mpld3 import display_d3

fig, ax = plt.subplots()
np.random.seed(0)
ax.plot(np.random.normal(size=100),
        np.random.normal(size=100),
        'or', ms=10, alpha=0.3)
ax.plot(np.random.normal(size=100),
        np.random.normal(size=100),
        'ob', ms=20, alpha=0.1)

ax.set_xlabel('this is x')
ax.set_ylabel('this is y')
ax.set_title('Matplotlib Plot Rendered in D3!', size=14)
ax.grid(color='lightgray', alpha=0.7)

display_d3(fig)

