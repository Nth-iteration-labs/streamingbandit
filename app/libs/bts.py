# -*- coding: utf-8 -*-
# Implementation of Bootstrap Thompson Sampling 
# Implemented for LM models
# TODO!
from libs.base import *
import libs.lm as lm
import numpy as np
import inspect
import collections
import ast

class BTS():
    """ Class to implement BTS.

    """
    def __init__(self, params, update_method = None,  m = 10):

        if isinstance(params,dict):
            if len(params) != m:
                self.params = {i : params.copy() for i in range(0,m)}
                self.params = collections.OrderedDict(self.params)
            else:
                self.params = {int(k) : ast.literal_eval(v).copy() for k,v in params.copy().items()}
                self.params = collections.OrderedDict(self.params)
                print(self.params)
        else:
            raise ValueError("Parameters should be a dict or a dict of dicts")

        #WORKS
        if update_method == None:
            raise ValueError("No update method or policy defined")
        if inspect.isclass(update_method):
            self.update_method = update_method
        elif not inspect.isclass(update_method):
            raise ValueError("Provided update method is not a class")

    def sample(self):
        select = np.random.choice(len(self.params))
        return self.params[select]

    def update(self, y, x, *args):
        draws = np.random.binomial(1,.5,len(self.params))
        print(draws)
        for i in range(0, len(self.params)):
            if draws[i] == 1:
                model = self.update_method(self.params[i], *args)
                model.update(y,x)
                self.params[i] = model.get_dict()

    def get_dict(self):
        return dict(self.params)
