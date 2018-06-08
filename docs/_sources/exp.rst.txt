Experiment functions
====================
Here we describe the **Experiment** class. This class, and its associated methods, allow accessing and storing policy parameters, logging data, and nesting experiments.

Note that the **Experiment** class is used in two ways in StreamingBandit:

1. The **getaction** and **setreward** code of an experiment are both executed within the scope of the **Experiment** class. Hence, here you can use **self.METHOD** to use the methods described below. 
2. Within an experiment, you can instantiate a new experiment by referring to its experiment **id** (thus by using **exp_nested = Experiment(exp_id = id1))**). You can subsequently execute the **getaction** and **setreward** code of this experiment. This functionality allows nesting of multiple experiments.

.. automodule:: core.experiment
.. autoclass:: Experiment
   :members: set_theta, get_theta, run_context_code, run_action_code, run_get_reward_code, run_reward_code, log_data
