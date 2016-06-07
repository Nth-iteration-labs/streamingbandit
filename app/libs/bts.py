# -*- coding: utf-8 -*-
# Implementation of Bootstrap Thompson Sampling 
# Implemented for LM models
# TODO!
from libs.base import *
import libs.lm as lm
import numpy as np

class BTS():
    """ Class to implement BTS.

    """
    def __init__(self, params, update_method = None,  m = 100):

        if len(params) == 1 and isinstance(params,list):
            self.params = [params[0].copy() for i in range(0,m)]
        elif isinstance(params,dict):
            self.params = [params.copy() for i in range(0,m)]
        else:
            raise ValueError("Parameters should be a list of dicts or a dict")

        if update_method = None:
            raise ValueError("No update method or policy defined")
        if inspect.isclass(update_method):
            self.update_method = update_method
        elif not inspect.isclass(update_method):
            raise ValueError("Provided update method is not a class")

    def sample(self):
        select = np.random.choice(len(self.params))
        return params[select]

    def update(self, y, x, *args):
        draws = np.random.binomial(1,.5,len(self.params))
        for i in range(0, len(self.params)):
            if draws[i] == 1:
                model = self.update_method(self.params[i], *args)
                model.update(y,x)
                self.params[i] = model.get_dict()
            return True

    def get_dict(self):
        return self.params
