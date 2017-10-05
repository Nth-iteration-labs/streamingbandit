# Generate random rewards for Condition and Treatment
import numpy as np
if self.action["treatment"] == "1":
    self.reward["value"] = np.random.normal(0, 1)
else:
    self.reward["value"] = np.random.normal(1, 2)
