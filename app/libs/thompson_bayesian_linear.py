# -*- coding: utf-8 -*-
import numpy as np
from libs.base import *
import ast

class ThompsonBayesianLinear():

    """ Class for Thompson sampling for Bayesian Linear Regression
    """
    def __init__(self, default):
        if default == {}:
            self.value = {'J' : [0, 0], 'P' : [[1, 0],[0, 1]], 'cov' : 1}
        else:
            self.value = default.copy()
        if isinstance(self.value['J'], str) == True:
            self.value['J'] = ast.literal_eval(self.value['J'])
        if isinstance(self.value['P'], str) == True:
            self.value['P'] = ast.literal_eval(self.value['P'])
        if isinstance(self.value['cov'], str) == True:
            self.value['cov'] = ast.literal_eval(self.value['cov'])
        self.value['J'] = np.matrix(self.value['J'])
        self.value['P'] = np.matrix(self.value['P'])

    def get_dict(self):
        self.value['J'] = self.value['J'].tolist()
        self.value['P'] = self.value['P'].tolist()
        return self.value

    def update(self, y, x):
        # Update J and P
        y = np.array(y)
        x = np.array(x)
        self.value['J'] = self.value['J'] + ((y*x.T)/self.value['cov'])
        self.value['P'] = self.value['P'] + ((x.T*x)/self.value['cov'])
    
    def sample(self):
        # Transform J = Sigma^-1 * mu to mu
        # Not sure if this is right?
        mu = self.value['J'] * np.linalg.inv(self.value['P'])
        mu = np.squeeze(np.asarray(mu))
        # Transform P = Sigma^-1 to Sigma
        sigma = np.linalg.inv(self.value['P'])
        # Random draw from np.random.multivariate_normal
        betas = np.random.multivariate_normal(mu, sigma)
        # Prediction is y_t ~ N(betas.T * x, sigma^2)
        #y = np.random.normal(np.dot(betas.T, x), cov)
        return betas
