********************
Complete RESTful API
********************

Here we describe the details of the REST API endpoints that are provided by StreamingBandit. Note that, with the exception of the two Core API calls, all the calls require authentication (for details see the Login API specs below).

Core API
--------
The core API contains the **getaction** and **setreward** calls (or, alternatively the decision and summary step of a bandit policy).

.. autotornado:: app:application
   :endpoints: ActionHandler.get, RewardHandler.get

Stats API
---------
The Stats API provides endpoints to retrieve data concerning running experiments. It is possible to retrieve the current state of the stored parameters, retrieve logged data, or retrieve summaries regarding the use of an experiment.

.. autotornado:: app:application
   :endpoints: GetCurrentTheta.get, GetHourlyTheta.get, GetLog.get, GetActionLog.get, GetRewardLog.get, GetSimulationLog.get, GetSummary.get

Evaluation API
--------------
The evaluation API provides the functionality to simulate the running of an experiment. Simulation will execute, in sequence, the **getcontext**, **getaction**, **getreward**, and **setreward** code as specified when creating a new experiment.

.. autotornado:: app:application
   :endpoints: Simulate.get

Admin API
---------
The admin endpoints provide the functionality to create, alter, and delete experiments.

.. autotornado:: app:application
   :endpoints: GenerateExperiments.post, GenerateExperiments.get, ListDefaults.get, GetDefault.get, UpdateExperiment.get, UpdateExperiment.delete, UpdateExperiment.put, ResetExperiment.get, AddUser.post

Login API
---------
The login API provides secure authentication.

.. autotornado:: app:application
   :endpoints: LogInHandler.post, LogOutHandler.get
