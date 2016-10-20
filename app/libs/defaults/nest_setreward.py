# Based on the experiment id we know which experiment to update
exp_id = self.action["Experiment"]
action = self.action["action"]
reward = self.reward["reward"]

exp_nested = Experiment(exp_id)
exp_nested.run_reward_code(context = self.context, action = action, reward = reward)
