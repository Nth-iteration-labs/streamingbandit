policies = ["18aec502c2", # E-Greedy
            "275fc0a66"] # E-First

for exp_id in policies:
    exp_nested = Experiment(exp_id)
    suggestion = exp_nested.run_action_code(context = {})
    if suggestion["treatment"] == self.action["treatment"]:
        mean = base.Mean(self.get_theta(key = "policy_means”, value = exp_id))
        mean.update(self.reward["value"])
        self.set_theta(mean, key = "policy_means”, value = exp_id)
        exp_nested.run_reward_code(context = {}, action = self.action, reward = self.reward)