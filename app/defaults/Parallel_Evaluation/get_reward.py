import numpy as np
if self.action["treatment"] == "C":
    self.reward["value"] = np.random.binomial(1,0.2)
else:
    self.reward["value"] = np.random.binomial(1,0.5)