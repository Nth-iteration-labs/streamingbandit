# Based on the exp_id we know which experiment to update
exp_id = self.action["experiment"]

exp_nested = Experiment(exp_id = exp_id)
exp_nested.run_reward_code(context = self.context, action = self.action, reward = self.reward)