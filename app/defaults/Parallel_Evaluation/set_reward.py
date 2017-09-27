action = self.action["action"]
reward = self.reward["reward"]
policies = [1, 2] # Fill in the exp_id's of the policies

for exp_id in policies:
    exp_nested = Experiment(exp_id)
    suggestion = exp_nested.run_action_code(context = {})
    if suggestion["action"] == action:
        exp_nested.run_reward_code(context = {}, action = action, reward = reward)
