# -*- coding: utf-8 -*-
# Wrapper for easy use of SciKit learn models
from libs.base import *
import numpy as np
import pickle

global numpy

## OK, this could just work, but its not tested
## And, we should use some kind of *args to pass multiple arguments...


class SKLModel:

    def __init__(self, value = {}, skClass="linear_model", skMethod="SGDRegressor"):
        
        if (value == {}):
            skClass = "linear_model"
            skM = self._skimport("sklearn."+skClass)
            self.Model = getattr(skM, "SGDRegressor")()   
        else:
            self.Model = pickle.loads(value["picklestr"])
       
    def get_dict(self):
        """ Return a dictionary with key:"picklestring" and \
            value:pickle.dumps(model)
            Used to store the model as a pickle object in database.
        """
        s = pickle.dumps(self.Model)
        return {"picklestr":s}

    def update(self, X=np.array([[]]), y=np.array([])):
        """ Update the linear model.

        :param np.array X: Multi dimensional array (matrix) with n rows of p features.
        :param np.array y: Array with n targets
        
        n can be 1 for incremental updates (default)
        """ 
        self.Model.partial_fit(X,y)
        
    def predict(self, X=np.array([[]])):
        """ Predict the output/observation value based on p features

        :param np.array X: Multi dimensional array (matrix) with n rows of p features.
        
        Mostly, X will have n=1 for a single prediction
        """
        return self.Model.predict(X)
        
    def _skimport(name):
        m = __import__(name)
        for n in name.split(".")[1:]:
            m = getattr(m, n)
        return m
