# Linear regression
from list.base import *
# See lecture notes AI webscale

class Model():
    
    def __init__(self, default): 
        self.value = default.copy()

    def get_dict(self):
        self.value['a'] = self.value['a'].tolist()
        self.value['b'] = self.value['b'].tolist()
        return self.value

    def get_coefs(self):
        beta = np.dot(np.linalg.inv(self.value['a']), self.value['b'])
        return #beta = A^-1 * B

    def update(self,y,x):
        y = np.array(y)
        x = np.array(x)
        self.value['a'] = self.value['a'] + (np.dot(x,np.transpose(x)))
        self.value['b'] = self.value['b'] + (np.dot(x,y)

