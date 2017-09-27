# Based on the exp_id we know which experiment to update
exp_id = self.action["Experiment"]
action = self.action["Treatment"]
reward = self.reward["Value"]

exp_nested = Experiment(exp_id = exp_id)
exp_nested.run_reward_code(context = self.context, action = action, reward = reward)
