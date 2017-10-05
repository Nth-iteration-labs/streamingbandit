# Based on the exp_id we know which experiment to update
exp_id = self.action["experiment"]
action = self.action["treatment"]
reward = self.reward["value"]

exp_nested = Experiment(exp_id = exp_id)
exp_nested.run_reward_code(context = self.context, action = action, reward = reward)
