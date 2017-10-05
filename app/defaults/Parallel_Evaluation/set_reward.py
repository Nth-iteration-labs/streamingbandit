policies = ["275fc0a66", "18aec502c2"] # Fill in the exp_id's of the policies

for exp_id in policies:
    exp_nested = Experiment(exp_id)
    suggestion = exp_nested.run_action_code(context = {})
    if suggestion["treatment"] == self.action["treatment"]:
        print(exp_id)
        exp_nested.run_reward_code(context = {}, action = self.action, reward = self.reward)
