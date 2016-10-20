import numpy as np

maxpercentage = self.context['maxpercentage']

split = np.random.uniform()
y = split * maxpercentage

self.action['split'] = split
self.action['y'] = y # The discount presented to the customer
