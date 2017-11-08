Complete RESTful API
====================

Core API
--------

.. autotornado:: app:application
   :endpoints: ActionHandler.get, RewardHandler.get

Stats API
---------

.. autotornado:: app:application
   :endpoints: GetCurrentTheta.get, GetHourlyTheta.get, GetLog.get, GetActionLog.get, GetRewardLog.get, GetSimulationLog.get, GetSummary.get

Evaluation API
--------------

.. autotornado:: app:application
   :endpoints: Simulate.get

Admin API
---------

.. autotornado:: app:application
   :endpoints: GenerateExperiments.post, GenerateExperiments.get, ListDefaults.get, GetDefault.get, UpdateExperiment.get, UpdateExperiment.delete, UpdateExperiment.put, ResetExperiment.get, AddUser.post

Login API
---------

.. autotornado:: app:application
   :endpoints: LogInHandler.post, LogOutHandler.get
