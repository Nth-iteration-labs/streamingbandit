# Linear regression
from list.base import *
# See lecture notes AI webscale

class Model():
    
    def __init__(self, default, p=len(default['b']), add_intercept=True):  # p meegeven op een of andere manier (int)
        # Initialize vector $b=0$, and matrixs $A = aI$
        # Possible extension: add ridge penalty.
        self.value = default.copy()
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
        
    def predict(self,x):
        x = np.array(x)
        beta = np.dot(np.linalg.inv(self.value['A']), self.value['b'])
        return np.dot(beta, x)