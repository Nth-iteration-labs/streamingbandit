# Linear regression
from list.base import *
# See lecture notes AI webscale

class Model():
    
    def __init__(self, default = {'b': [0 0], 'A': [[1, 0],[0 1]], 'n':0}, p=None, add_intercept=True):  # p meegeven op een of andere manier (int)
        # Initialize vector $b=0$, and matrixs $A = aI$
        if default == {}:
            self.value = {'b': [0 0], 'A': [[1, 0],[0 1]], 'n':0}
        else:
            self.value = default.copy()
        if p is None:
            self.p = len(self.value['b'])
        self.value['A'] = np.array(self.value['A'])
        self.value['b'] = np.array(self.value['b'])
        # Possible extension: add ridge penalty.
        self.intercept = add_intercept # If true, add intecept to p (thus p=p+1, and standard add 1 to x)

    def get_dict(self):
        # A is p*p matrix ()
        # b is 1*p vector
        self.value['A'] = self.value['A'].tolist()
        self.value['b'] = self.value['b'].tolist()
        # Add n (counter): later use for Standard errors of Beta.
        return self.value

    def get_coefs(self):
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'])
        return beta

    def update(self,y,x):
        y = np.array(y)
        x = np.array(x)
        self.value['A'] = self.value['A'] + (np.dot(x,np.transpose(x)))
        self.value['b'] = self.value['b'] + (np.dot(x,y))
        self.value['n'] = self.value['n'] + 1
        
    def predict(self,x):
        x = np.array(x)
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'])
        return np.dot(beta, x)
