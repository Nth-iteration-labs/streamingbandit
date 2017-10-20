if not("condition" in self.get_theta("userid", self.context["userid"])):
    self.action["note"] = "First allocation"
    import random
    draw = random.choice(["baseline", "random", "lockin"])
    self.set_theta({"condition":draw}, "userid", self.context["userid"])

self.action["condition"] = self.get_theta("userid", self.context["userid"])["condition"]