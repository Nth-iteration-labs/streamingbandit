maxpercentage = self.context['maxpercentage']
split = np.random.uniform()
discount = split * maxpercentage
self.action['split'] = split 
self.action['discount'] = discount