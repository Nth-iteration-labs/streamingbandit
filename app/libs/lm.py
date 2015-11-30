# Linear regression
from libs.base import *
# See lecture notes AI webscale

class Model():
    """ Class to interpet a linear model.

    :variable dict default: The value of the model, consisting of a 1*p
    list of b, p*p list of lists A and counter n.
    :variable int p: Number of estimators.
    :variable bool add_intercept: If True, the update function expects that
    there it has to add the intercept to the X vector itself.
    """
    def __init__(self, default = {'b': [0 0], 'A': [[1, 0],[0 1]], 'n':0}, p=None, add_intercept=True):  # p meegeven op een of andere manier (int)
        """ Class to fit a linear model with a sequential solution for linear
        regression.
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
        """ Return all the variables that are needed to do an online estimation
        in a dictionary.
        """
        # A is p*p matrix ()
        # b is 1*p vector
        self.value['A'] = self.value['A'].tolist()
        self.value['b'] = self.value['b'].tolist()
        # Add n (counter): later use for Standard errors of Beta.
        return self.value

    def get_coefs(self):
        """ Returns the coefficients beta as a numpy array.
        """
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'])
        return beta

    def update(self,y,x):
        """ Update the linear model.

        :param int y: The observation value.
        :param list x: A list of ints of the regressors. 
        """ 
        y = np.array(y)
        x = np.array(x)
        if self.intercept:
            x = np.insert(x, 0, 1)
        self.value['A'] = self.value['A'] + (np.dot(x,np.transpose(x)))
        self.value['b'] = self.value['b'] + (np.dot(x,y))
        self.value['n'] = self.value['n'] + 1
        
    def predict(self,x):
        """ Predict the output/observation value based on values for
        the regressors.

        :param list x: A list of ints of the regressors.
        :param numpy y: A numpy array of the predicted observation.
        """
        x = np.array(x)
        if self.intercept:
            x = np.insert(x, 0, 1)
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'])
        return np.dot(beta, x)
