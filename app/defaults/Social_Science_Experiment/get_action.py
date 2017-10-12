if not("condition" in self.get_theta("userid", self.context["userid"])):
    self.action["note"] = "Allocate"
    import random
    draw = random.sample(["baseline", "random", "lockin"],1)
    self.set_theta({"condition":draw}, "userid", self.context["userid"])

self.action["condition"] = self.get_theta("userid", self.context["userid"])["condition"]