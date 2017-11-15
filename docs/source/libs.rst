Documentation of the supplied Libraries
=======================================
StreamingBandit is build on a philosophy of streaming (or online, or row-by-row) updating of parameters of a policy. The **libs** libraries provide some functionality for estimating and fitting statistical models online. These libraries are available directly in the **getaction** and **setreward** code.

The following code provides an example of the use of one of the **libs** in the **getaction** code of an experiment:
.. highlight:: python
   :linenothreshold: 1
mean_list = base.List(
             self.get_theta(key="treatment"), 
             base.Mean, ["control", "treatment"]
             )
self.action["treatment"] = meanList.max()
.. highlight:: 
which would retrieve a list of sample means by name (**treatment** and **control**), and subsequently select the name with the highest mean. 

Note that each of the **libs** provides update methods to update the object when new data is observed. For example, the code:
.. highlight:: python
   :linenothreshold: 1
mean = base.Mean(
     self.get_theta(
     key="treatment", value=self.action["treatment"])
     )
mean.update(self.reward["value"])
.. highlight:: 
can be used in the **setreward** code to retrieve the mean specified in the **treatment** variable, and subsequently update it using the **value**

Below we detail the current **libs** and each of their methods.

Base classes
************
The base classes provide the functionality to create, store, and update (lists of) counts, means, variances, proportions, and co-variances in data streams.

.. automodule:: libs.base
   :members:
   :special-members:

Linear Regression
*****************
The linear regression library allows online fitting of a linear regression model using OLS.

.. automodule:: libs.lm
   :members:
   :special-members:

Thompson sampling
*****************
This library implements Thompson sampling for the k-armed Bernoulli bandit as well as Thompson sampling for optimal design of experiments (Thompson sampling based on the posterior variance of the observed outcome). See also `this paper <https://link.springer.com/article/10.3758/s13428-014-0480-0>`_.

.. automodule:: libs.thompson
   :members:
   :special-members:

Bootstrapped Thompson Sampling
******************************
This library provides the functionality to perform on online bootstrap of any streaming estimate obtained by the **libs** and subsequently implements Bootstrap Thompson Sampling (BTS, `see this paper <https://arxiv.org/abs/1410.4009>`_ for details).

.. automodule:: libs.bts
   :members:
   :special-members:

Lock-in Feedback
****************
This library provides a (1D) implementation of Lock-in Feedback. See `this paper <https://arxiv.org/abs/1502.00598>`_ for details.

.. automodule:: libs.lif
   :members:
   :special-members:

Thompson Bayesian Linear Regression
***********************************
This library implements (online) Bayesian linear regression and Thompson sampling based on the posterior Beta's.

.. automodule:: libs.thompson_bayesian_linear
   :members:
   :special-members:
