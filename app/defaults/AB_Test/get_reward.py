# Generate random rewards for each treatment
if self.action["treatment"] == "1":
    self.reward["value"] = np.random.binomial(1,0.5)
else: #Treatment = 2
    self.reward["value"] = np.random.binomial(1,0.3)
