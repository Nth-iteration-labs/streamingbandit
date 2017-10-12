# Generate random rewards for Condition and Treatment
import numpy as np
if self.action["treatment"] == "condition":
    self.reward["value"] = np.random.normal(4, 1)
else:
    self.reward["value"] = np.random.normal(6, 2)