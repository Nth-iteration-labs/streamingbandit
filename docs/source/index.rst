Welcome to StreamingBandit's documentation!
===========================================

This is the official documentation for StreamingBandit. You can find the source
code at `GitHub`_.

.. _GitHub: https://github.com/nth-iteration-labs/streamingbandit

About StreamingBandit
=====================

StreamingBandit is a RESTful API web application for developing and testing sequential experiments in field and simulation studies. This is done by formalizing a sequential experiment as a `(contextual) multi-armed bandit problem <https://en.wikipedia.org/wiki/Multi-armed_bandit>`_. Each sequential experiment can be defined as follows. At each interaction :math:`t`:
    
    1. the experimenter observes a *context* :math:`x_t`,
    2. subsequently, the experimenter chooses an *action* :math:`a_t`,
    3. and finally a *reward* :math:`r_t` is observed.
    
The main aim of the experimenter is to maximize the cumulative reward :math:`\sum_{t=1}^N r_t` where :math:`N` denotes the total number of interactions. To do so, the experimenter applies a *policy* :math:`\pi` which is some function that takes the context :math:`x_t` and the historical interactions, and returns an action. For convenience we denote all historical interactions using :math:`\mathcal{D}_{(t-1)}` and thus we have :math:`\pi(x_t, \mathcal{D}_{t-1}) \rightarrow a_t`. 

The following are some examples of when StreamingBandit is a useful tool:

* Personalized healthcare: A physician meets with patients sequentially. For each patient she observes a number of background characteristics (gender, age, current condition) constituting the context. Subsequently, her action is to choose a treatment such that the reward—measured in terms of general health of the patient—is maximized.
* Online advertising: In online advertising a firm selecting an ad observes the context consisting of a description of the current user visiting a specific webpage. The action is to choose an advertisement out of a set of possible advertisements (possibly dependent on the context itself), and the rewards constitute the clicks on the ad.
* Product recommendation systems: The context denotes all that is known about the user at a certain point in time. The action is choosing one out of a set of products, and the reward consists of the revenue generated at each interaction.
* Social science experiments: Many social science experiments constitute a special case of contextual decision making: during the experiment participants are recruited sequentially. The context consists of all that’s known about the participant, and sequently the action is to assign a participant to a specific experimental condition (possibly dependent on the context in cases of, e.g., stratified sampling). Finally, the reward(s) consist of the outcome measures of the experiments.

The list above illustrates the generality of our approach; StreamingBandit can be used to allocate actions in all of the above applications.

To ensure the computational scalability of StreamingBandit, we assume that at the latest interaction :math:`t=t'`, all the information necessary to choose an action can be summarized using a limited set of parameters denoted :math:`\theta_{t'}`, where often the dimensionality of :math:`\theta_t` is (much) smaller than that of :math:`\mathcal{D}_{t-1}`. Given this assumption, we identify the following two steps of a policy:

1. The *decision* step: In the decision step, using :math:`x_{t'}` and :math:`\theta_{t'}`, and often using some (statistical) model relating the actions, the context, and the reward which is parametrized by :math:`\theta_{t'}`, a next action :math:`a_{t'}` is selected. Making a request to StreamingBandit's **getaction** REST endpoint returns a JSON object containing the selected action. Optionally, you can request an **advice_id** that will couple your **getaction** to your **setreward** call - more info on this is inside the Experiment documentation.
2. The *summary* step: In each summary step :math:`\theta_{t'}` is updated using the new information :math:`\{x_{t'},a_{t'},r_{t'}, p_{t'}\}`. Thus, in this step, :math:`\theta_{t'+1} = g(\theta_{t'}, x_{t'},a_{t'},r_{t'}, p_{t'})` where :math:`g()` is some update function. Effectively, all the prior data, :math:`\mathcal{D}_{t-1}` are *summarized* into :math:`\theta_{t'}`. This choice makes that the computations are bounded by the dimension of :math:`\theta` and the time required to update :math:`\theta` instead of growing as a function of :math:`t`. Note that this effectively forces users to implement an online policy; the complete dataset :math:`\mathcal{D}_{t-1}` is not revisited at subsequent interactions. Making a request to StreamingBandit's **setreward** endpoint containing a JSON object including either the **advice_id**, or a complete description of :math:`\{x_{t'},a_{t'}, p_{t'}\}`, and the reward :math:`r_{t'}`, allows one to update :math:`\theta_{t'+1}` and subsequently influence the actions selected at :math:`t'+1`.

For the basic usage of StreamingBandit the experimenter---or rather an external server or mobile application---sequentially executes requests to the **getaction** and **setreward** endpoints, and allocates actions accordingly. Using this setup, StreamingBandit can be used to, for example, sequentially select advertisements on webpages, allocate research subjects in an online experiment to different experimental conditions, or sequentially optimize the feedback provided to users off a mobile eHealth application.

For more information on how StreamingBandit works, check out the documentation and `this paper <https://arxiv.org/abs/1602.06700>`_.

Contributing to the libraries
=============================

We gladly accept any contribution to expanding the libraries of StreamingBandit.
However, we maintain a strict policy for further development to ensure that the master branch of the project is always clean. 
We encourage contributors to checkout of the dev branch on a fork of the repository, create a new feature branch (using “f/<feature_name>”, where f stands for feature), and submit a merge request to the dev branch once additions have been thoroughly tested and documented. 
Merge requests that are not accompanied with thorough documentation will be rejected. 
Once tested by the team of maintainers, updates are pushed to the dev branch and subsequently to the main branch (and the Docker distribution) as quickly as possible.

The libraries that are currently written are all tested and have a default that
functions with them.
If you would like to contribute by writing a part of the library, look at the
following points:

* Write a Base class according to the skeleton class __strmBase.
* Write a default example of a use-case of the class in the defaults folder. This should include at least two but preferably four of the following files:

    * getContext.py (optional)
    * getAction.py
    * getReward.py (optional)
    * setReward.py

Providing all four files makes it easier to test, simulate and use your newly implemented policy. Make sure that you develop your new library inside your own fork of StreamingBandit. Again, after you have tested your policy and library, you can create a pull request which we will review.

Furthermore, we also encourage users to request features in the issues section in the main repository, which our team can discuss and possibly implement.


Authors
=======

Maurits Kaptein (``maurits at mauritskaptein dot com``)

Jules Kruijswijk (``juleskruijswijk at gmail dot com``)

Robin van Emden (``robin at pwy dot nl``)

.. toctree::
   :hidden:

   Introduction <self>
   Installation <install>
   API <api>
   Libs <libs>
   Experiment <exp>
