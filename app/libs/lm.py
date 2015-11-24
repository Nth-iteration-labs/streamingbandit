# Linear regression
from list.base import *
# See lecture notes AI webscale

class Model():
    """ Class to fit a linear model with a sequential solution for linear
    regression.
    """
    def __init__(self, default = {'b': [0 0], 'A': [[1, 0],[0 1]], 'n':0}, add_intercept=True):  # p meegeven op een of andere manier (int)
        """ Create an instance of a linear model.

        :param dict default: A dict containing a vector b, matrix A and scalar
        n. b should be a 1*p vector and A a p*p matrix (where p is the number
        of predictors for the model.
        :param bool add_intercept: Standard set to True. If True, then when
        updating the model, the vector x does not need to contain the
        intercept.
        """
        # Initialize vector $b=0$, and matrixs $A = aI$
        if default == {}:
            self.value = {'b': [0 0], 'A': [[1, 0],[0 1]], 'n':0}
        else:
            self.value = default.copy()
        self.p = len(self.value['b'])
        self.value['A'] = np.array(self.value['A'])
        self.value['b'] = np.array(self.value['b'])
        # Possible extension: add ridge penalty.
        self.intercept = add_intercept # If true, add intecept to p (thus p=p+1, and standard add 1 to x)

    def get_dict(self):
        """ Get dictionary with the b, A and n (for example to store in a
        database.
        """
        # A is p*p matrix ()
        # b is 1*p vector
        self.value['A'] = self.value['A'].tolist()
        self.value['b'] = self.value['b'].tolist()
        # Add n (counter): later use for Standard errors of Beta.
        return self.value

    def get_coefs(self):
        """ Get the coefficients (beta's) of the linear model.
        """
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'])
        return beta

    def update(self,y,x):
        """ Update the linear model

        :param int y: The output value y.
        :param list x: List with values of regressors X.
        """
        y = np.array(y)
        x = np.array(x)
        if self.intercept:
            x = np.insert(x, 0, 1)
        self.value['A'] = self.value['A'] + (np.dot(x,np.transpose(x)))
        self.value['b'] = self.value['b'] + (np.dot(x,y))
        self.value['n'] = self.value['n'] + 1
        
    def predict(self,x):
        """ Given an vector of regressors X, give most probable value of y.

        :param list x: List with values of regressors X.
        """
        x = np.array(x)
        if self.intercept:
            x = np.insert(x, 0, 1)
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'])
        return np.dot(beta, x)
