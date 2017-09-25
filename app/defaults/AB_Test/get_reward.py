# Generate random rewards for each treatment
import numpy as np
self.reward['value'] = np.random.binomial(1,1/int(self.action['Treatment']))
