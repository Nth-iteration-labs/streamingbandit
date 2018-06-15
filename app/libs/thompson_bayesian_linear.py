# -*- coding: utf-8 -*-
import numpy as np
from libs.base import *
import ast

global numpy

class ThompsonBayesianLinear():
    """ Class for Thompson sampling for Bayesian Linear Regression
    
    :var dict default: The value of the model, consisting of a 1*p \
    list of J, p*p list of P and an error rate.
    """
    def __init__(self, default):
        if default == {}:
            self.value = {'J' : [0, 0], 'P' : [[1, 0],[0, 1]], 'err' : 1}
        else:
            self.value = default.copy()
        if isinstance(self.value['J'], str) == True:
            self.value['J'] = ast.literal_eval(self.value['J'])
        if isinstance(self.value['P'], str) == True:
            self.value['P'] = ast.literal_eval(self.value['P'])
        if isinstance(self.value['err'], str) == True:
            self.value['err'] = ast.literal_eval(self.value['err'])
        self.value['J'] = np.matrix(self.value['J'])
        self.value['P'] = np.matrix(self.value['P'])

    def get_dict(self):
        """ Return all the variables that are needed to do an online estimation \
        in a dictionary. Or to save the parameters in a database.
        """
        to_dict = self.value.copy()
        to_dict['J'] = to_dict['J'].tolist()
        to_dict['P'] = to_dict['P'].tolist()
        return to_dict

    def update(self, y, x, discount = 1):
        """ Update the Bayesian linear model.
        
        :param int y: The observation value.
        :param list x: A list of ints of the regressors.
        :param int discount: A discount. Default is 1, which means no discount is used.
        """
        y = y
        x = np.matrix(x)
        self.value['J'] = (discount*(x*y)/self.value['err']) + self.value['J']
        self.value['P'] = (discount*(x.T*x)/self.value['err']) + self.value['P']
    
    def sample(self):
        """ Return a sample of coefficients Betas using Thompson sampling.

        """
        # Transform J = Sigma^-1 * mu to mu
        # Transform P = Sigma^-1 to Sigma
        sigma = np.linalg.inv(self.value['P'])
        mu = sigma * self.value['J'].T
        mu = np.squeeze(np.asarray(mu))
        # Random draw from np.random.multivariate_normal
        betas = np.random.multivariate_normal(mu,sigma)
        # Prediction is y_t ~ N(betas.T * x, sigma^2)
        #y = np.random.normal(np.dot(betas.T, x), err)
        return betas
