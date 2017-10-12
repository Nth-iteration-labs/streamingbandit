policies = ["3ea45886b5", "121e3e0aeb"] # Fill in the exp_id's of the policies

# Implement li et al.
for exp_id in policies:
    exp_nested = Experiment(exp_id)
    suggestion = exp_nested.run_action_code(context = {})
    if suggestion["treatment"] == self.action["treatment"]:
        exp_nested.run_reward_code(context = {}, action = self.action, reward = self.reward)
        
        # add a way of computing the mean reward!