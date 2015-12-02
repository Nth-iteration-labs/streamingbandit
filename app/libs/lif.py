# Implementation of Lock in Feedback.
# -*- coding: utf-8 -*-
from libs.base import *
import numpy as np
import json

class Lif:

    def __init__(self, theta, x0=1.0, A=1.4, T=100, gamma=.004, omega=0.8, lifversion=2):
        self._set_parameters(x0, A, T, gamma, omega, lifversion)
        self._set_theta(theta)

    def _set_parameters(self, x0, A, T, gamma, omega, lifversion):
        self.x0 = x0
        self.A = A
        self.T = T
        self.gamma = gamma
        self.omega = omega
        self.lifversion = lifversion

    def _set_theta(self,theta):
        if theta == None:
            self.theta = {'Yw': self._np_nan_fill(self.T, 3), 't':0, 'x0':self.x0}
        else:
            self.theta = json.loads(str(theta))
            self.theta['Yw'] = np.array(self.theta['Yw'])
            self.theta['t']  = int(self.theta['t'])
            self.theta['x0']  = float(self.theta['x0'])

    def get_theta(self):
        theta_serial = self.theta
        theta_serial['Yw'] = theta_serial['Yw'].tolist()
        theta_serial = json.dumps(theta_serial)
        return theta_serial

    def get_x0(self):
        return self.theta['x0']

    def suggest(self):
        self.theta['t'] = self.theta['t'] + 1
        x = self.theta['x0'] + self.A*np.cos(self.omega * self.theta['t'])
        suggestion = {'x': x, 't':self.theta['t'], 'x0': self.theta['x0']}

        if np.all(np.isfinite(self.theta['Yw'][:,0])):
            self.theta['x0'] = np.mean(self.theta['Yw'][:,1])
            self.theta['x0'] = self.theta['x0'] + self.gamma * sum( self.theta['Yw'][:,2] )
            if self.lifversion==1: self.theta['Yw'].fill(np.nan)

        return suggestion

    def update(self, t, x, y):

        y = self.A*np.cos(self.omega * t)*y
        row_to_add = np.array([t,x,y])
        self.theta['Yw'] = self._matrixpush(self.theta['Yw'], row_to_add)

        return True

    def _matrixpush(self, m, row):
        if not np.all(np.isfinite(self.theta['Yw'][:,0])):
            i = np.count_nonzero(np.logical_not(np.isnan(self.theta['Yw'][:,0])))
            m[i,] = row
        else:
            m = np.vstack([m,row])
            m = m[1:,]
        return(m)

    def _np_nan_fill(self,rows,columns):
        nan_values = np.zeros((rows,columns))
        nan_values.fill(np.nan)
        return nan_values