# Linear regression
from libs.base import *
import ast

class LM():
    """ Class to interpet a linear model.

    :variable dict default: The value of the model, consisting of a 1*p \
    list of b, p*p list of lists A and counter n.
    :variable int p: Number of estimators.
    :variable bool add_intercept: If True, the update function expects that \
    there it has to add the intercept to the X vector itself.
    """
    def __init__(self, default, p=None, add_intercept=True): 
        """ Class to fit a linear model with a sequential solution for linear \
        regression.
        """
        # Initialize vector $b=0$, and matrixs $A = aI$
        if default == {}:
            self.value = {'b': [0, 0], 'A': [[1, 0],[0, 1]], 'n':0}
        else:
            self.value = default.copy()
        self.p = len(self.value['b'])
        if isinstance(self.value['A'],str) == True:
            self.value['A'] = ast.literal_eval(self.value['A'])
        if isinstance(self.value['b'],str) == True:
            self.value['b'] = ast.literal_eval(self.value['b'])
        if isinstance(self.value['n'],str) == True:
            self.value['n'] = ast.literal_eval(self.value['n'])
        self.value['A'] = np.matrix(self.value['A'])
        self.value['b'] = np.matrix(self.value['b'])
        # Possible extension: add ridge penalty.
        self.intercept = add_intercept # If true, add intecept to p (thus p=p+1, and standard add 1 to x)

    def get_dict(self):
        """ Return all the variables that are needed to do an online \
              estimation in a dictionary.
        """
        # A is p*p matrix ()
        # b is 1*p vector
        to_dict = self.value.copy()
        to_dict['A'] = to_dict['A'].tolist()
        to_dict['b'] = to_dict['b'].tolist()
        # Add n (counter): later use for Standard errors of Beta.
        return to_dict

    def get_coefs(self):
        """ Returns the coefficients beta as a numpy array.
        """
        beta = np.linalg.inv(self.value['A']) * self.value['b'].T
        return beta

    def update(self,y,x,discount = 1):
        """ Update the linear model.

        :param int y: The observation value.
        :param list x: A list of ints of the regressors. 
        """ 
        y = y
        x = np.matrix(x)
        if self.intercept:
            x = np.insert(x, 0, 1)
        self.value['A'] = self.value['A'] + discount*(x.T*x)
        self.value['b'] = self.value['b'] + discount*(x*y)
        self.value['n'] = self.value['n'] + 1
        
    def predict(self,x):
        """ Predict the output/observation value based on values for \
        the regressors.

        :param list x: A list of ints of the regressors.
        :param numpy y: A numpy array of the predicted observation.
        """
        x = np.array(x)
        if self.intercept:
            x = np.insert(x, 0, 1)
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'].T)
        return np.dot(beta, x)
