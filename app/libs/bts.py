# -*- coding: utf-8 -*-
# Implementation of Bootstrap Thompson Sampling 
# Tested for LM models, but should work with others as well
from libs.base import *
import libs.lm as lm
import numpy as np
import inspect
import collections
import ast

class BTS():
    """ Class to implement BTS.

    :var dict params: If initialized, a dict of dicts, containing m samples of \
    parameters for the update_method/model that is being used. If not initialized \
    this will be made into a dict of dicts using the given params or default_params.
    :var Class update_method: A class reference containing the update method. \
    This will be checked and if it is a class, it will be used to update the parameters.
    :var int m: The number of bootstraps that BTS uses.
    :var dict default_params: A dictionary containing the default parameters. \
    If the params variable is empty/not long enough, this will be used.
    :var bool param_noise: If True, BTS will add parameter noise to all the lists \
    in the default_params dictionary when initializing the bootstraps.
    :var double noisesd: If param_noise is used, this is the standard deviation \
    used for adding noise using a Normal distribution.
    """
    def __init__(self, params, update_method = None,  m = 100, default_params = None, param_noise = True, noisesd = .1):

        if update_method == None:
            raise ValueError("No update method or policy defined")
        if inspect.isclass(update_method):
            self.update_method = update_method
        elif not inspect.isclass(update_method):
            raise ValueError("Provided update method is not a class")

        if isinstance(params,dict):
            if len(params) != m:
                if default_params is not None:
                    self.params = {}
                    for i in range(0,m):
                        tmp_params = {}
                        for k,v in default_params.items():
                            if isinstance(v, list) and param_noise == True:
                                tmp_params[k] = np.random.normal(v,noisesd).tolist()
                            else:
                                tmp_params[k] = v
                        self.params[i] = tmp_params.copy()
                    self.params = collections.OrderedDict(self.params)
                else:
                    self.params = {i : params.copy() for i in range(0,m)}
                    self.params = collections.OrderedDict(self.params)
            else:
                self.params = {int(k) : ast.literal_eval(v).copy() for k,v in params.copy().items()}
                self.params = collections.OrderedDict(self.params)
        else:
            raise ValueError("Parameters should be a dict or a dict of dicts")

    def sample(self):
        """ Return a sample of the m bootstraps.
        """
        select = np.random.choice(len(self.params))
        return self.params[select]

    def update(self, y, x, *args, **kwargs):
        """ Update the bootstraps using a double or nothing update policy.

        :param y: This may contain any type of class as long as the update_method \
        provided is able to parse this type.
        :param x: This may contain any type of class as long as the update_method \
        provided is able to parse this type.
        """
        draws = np.random.binomial(1,.5,len(self.params))
        for i in range(0, len(self.params)):
            if draws[i] == 1:
                model = self.update_method(self.params[i], *args)
                model.update(y,x, **kwargs)
                self.params[i] = model.get_dict()

    def get_dict(self):
        """ Return all the variables and bootstraps that are needed to do an online \
        estimation in a dictionary. Or to save the data into a database.
        """
        return dict(self.params)
