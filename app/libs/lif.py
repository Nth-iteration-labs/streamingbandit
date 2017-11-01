# Implementation of Lock in Feedback.
# -*- coding: utf-8 -*-
from libs.base import *
import numpy as np
import json


class LiF():
    """ Class implementing the Lock in Feedback algorithm.
    Implementation of Lock in Feedback, \
    following the definition by Maurits Kaptein and \
    Davide Iannuzzi in https://arxiv.org/abs/1502.00598.

    :var dict theta:  Theta, consisting of Yw, t, and x0.
    :var float x0: Start value of X.
    :var float A: Amplitude.
    :var int T: Integration time.
    :var float gamma: Learnrate.
    :var float omega: Omega.
    :var int lifversion: Either version 1 or 2.
    """

    def __init__(self, theta, x0=1.0, a=1.4, t=100, gamma=.004, omega=0.8, lifversion=2):
        """ Class implementing the Lock in Feedback algorithm.
        """
        
        self._set_parameters(x0, a, t, gamma, omega, lifversion)
        self._set_dict(theta)

    def _set_parameters(self, x0, a, t, gamma, omega, lifversion):
        """ Set the parameters.

        :param float x0: Start value of X.
        :param float A: Amplitude.
        :param int T: Integration time.
        :param float gamma: Learnrate.
        :param float omega: Omega.
        :param lifversion: Apply LiF version 1 or 2.
        """
        self.x0 = x0
        self.A = a
        self.T = t
        self.gamma = gamma
        self.omega = omega
        self.lifversion = lifversion

    def _set_dict(self, theta):
        """ Initialize or set theta.

        :param dict theta: Dict theta, consisting of Yw, t, and x0.
        """
        if theta == {}:
            self.theta = {'Yw': self._np_nan_fill(self.T, 3), 't': 0, 'x0': self.x0}
        else:
            self.theta = theta.copy()
            self.theta['Yw'] = np.array(json.loads(str(self.theta['Yw'])))
            self.theta['t'] = int(self.theta['t'])
            self.theta['x0'] = float(self.theta['x0'])

    def get_dict(self):
        """  Return dict theta.

        :returns:  Theta, consisting of Yw, t, and x0.
        """
        theta_dict = {'Yw': json.dumps(self.theta['Yw'].tolist()), 't': self.theta['t'], 'x0': self.theta['x0']}
        return theta_dict

    def suggest(self):
        """  Returns dict containing controlled variable x \
        oscillating with time t, the value of t itself and \
        the current x0.

        :returns:  Suggestion {x,t,x0}
        """
        if np.all(np.isfinite(self.theta['Yw'][:, 0])):
            self.theta['x0'] = self.theta['x0'] + self.gamma * sum(self.theta['Yw'][:, 2]) / self.T
            if self.lifversion == 1:
                self.theta['Yw'].fill(np.nan)

        self.theta['t'] += 1
        x = self.theta['x0'] + self.A * np.cos(self.omega * self.theta['t'])
        suggestion = {'x': x, 't': self.theta['t'], 'x0': self.theta['x0']}

        return suggestion

    def update(self, t, x, y, x0):
        """  Update LiF with outcome y at time t and at value x \
        integrating yω over a time T = 2πN.

        :param int t: time t.
        :param float x: controlled variable x.
        :param float y: outcome variable y.
        :returns: True
        """
        self.theta['x0'] = x0
        self.theta['t'] = t 
        y = self.A * np.cos(self.omega * t) * y
        row_to_add = np.array([t, x, y])
        self.theta['Yw'] = self._matrixpush(self.theta['Yw'], row_to_add)

        return True

    def _matrixpush(self, m, row):
        """  Numpy FIFO helper function, \
        pushes a row onto a matrix \
        and removes the oldest value if full.

        :param numpy.ndarray m: matrix.
        :param np.array row: row to be added to matrix.
        """
        if not np.all(np.isfinite(self.theta['Yw'][:, 0])):
            i = np.count_nonzero(np.logical_not(np.isnan(self.theta['Yw'][:, 0])))
            m[i, ] = row
        else:
            m = np.vstack([m, row])
            m = m[1:, ]
        return m

    def _np_nan_fill(self, rows, columns):
        """  Numpy helper function, \
        returns an nan-filled numpy.ndarray \
        matrix of rows x columns.

        :param int rows: matrix
        :param int columns: columns to be added to matrix
        """
        nan_values = np.zeros((rows, columns))
        nan_values.fill(np.nan)
        return nan_values
