if self.context["Type"] <= 5 and self.action["Price"] < 5:
    self.reward["Revenue"] = abs(np.random.normal(1, 0.1))
elif self.context["Type"] <= 5 and self.action["Price"] >= 5:
    self.reward["Revenue"] = abs(np.random.normal(0, 0.01))
elif self.context["Type"] > 5:
    self.reward["Revenue"] = abs(np.random.normal(5, 1))
