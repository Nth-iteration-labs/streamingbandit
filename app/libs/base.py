import numpy as np
#import json
#from scipy.optimize import minimize_scalar

class __strmBase(object):
    
    def __init__(self):
        self.value = False
        self.main = ''
        
    # THIS SHOULD BE IMPLEMENTED IN experiment.set_theta()
	# if isinstance(values, __strmBase):
	#	values = values.get_dict()
    def get_value(self):
        return self.value[self.main]

    def get_dict(self):
        return self.value
        
    # We might be able to make generic operators:
    def __add__(self, other):
        self.value[self.main] = int(self.value[self.main]) + int(other)

    def __sub__(self, other):
        self.value[self.main] = int(self.value[self.main]) - int(other)

    def __truediv__(self, other):
        self.value[self.main] = float(self.value[self.main]) / float(other)

    def __mul__(self, other):
        self.value[self.main] = float(self.value[self.main]) * float(other)


class Count(__strmBase):
    
    def __init__(self, default={'n':0}):
        self.main = 'n'
        self.value = default.copy()
    
    def update(self, value=1):
        self.__add__(value)
        
    def increment(self):
        self.value['n'] = int(self.value['n']) + 1
        

class Mean(Count):
    
    def __init__(self, default={'n':0, 'm':0}):
        self.main = 'm'
        self.value = default.copy()
        
    def update(self, value):
        self.value['n'] = int(self.value['n']) + 1
        current['m'] = float(self.value['m']) + ( (float(value) - float(self.value['m'])) / self.value['n'])
   
    def get_count(self):
        return self.value['n']

class Variance(__strmBase):

    def __init__(self, default={'n':0, 'x_bar':0, 's':0}):
        self.main = "p"
        self.value = default.copy()

    def update(self, value):
        old_n = int(self.value['n'])
        self.value['n'] = int(self.value['n']) + 1
        self.value['x_bar'] = value + ( (value - float(self.value['x_bar'])) / (old_n + 1) )
        self.value['s'] = float(self.value['s']) + ( (value - float(self.value['x_bar'])) * (value - float(self.value['x_bar'])) )

    def get_value(self):
        return float(self.value['s'])/(int(self.value['n']) - 1)

    def __add__(self, other):
        new_value = float(self.value[self.main]) + float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Variance can not be less than zero!") 

    def __sub__(self, other):
        new_value = float(self.value[self.main]) - float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Variance can not be less than zero!")

    def __truediv__(self, other):
        new_value = float(self.value[self.main]) / float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Variance can not be less than zero!")

    def __mul__(self, other):
        new_value = float(self.value[self.main]) * float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Variance can not be less than zero!")

class Proportion(__strmBase):

    def __init__(self,default={'p':.5, 'n': 2}):
        self.main = 'p'
        self.value = default.copy()

    def update(self, value):
        self.value['n'] = int(self.value['n']) + 1
        self.value['p'] = float(self.value['p']) + ( (value - float(self.value['p'])) / self.value['n'])

    def __add__(self, other):
        new_value = float(self.value[self.main]) + float(other)
        if 0 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Proportion must be between 0 and 1!")

    def __sub__(self, other):
        new_value = float(self.value[self.main]) - float(other)
        if 0 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Proportion must be between 0 and 1!")

    def __truediv__(self, other):
        new_value = float(self.value[self.main]) / float(other)
        if 0 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Proportion must be between 0 and 1!")

    def __mul__(self, other):
        new_value = float(self.value[self.main]) * float(other)
        if 0 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Proportion must be between 0 and 1!")

class Covariance(__strmBase):

    def __init__(self,default={'n':0, 'x_bar':0, 'y_bar':0, 'cov':0}):
        self.main = 'cov'
        self.value = default.copy()

    def update(self, value):
        # Value must be a dict of x and y as
        # {'x' : 0, 'y' : 0} since we compute covariance of two datapoints
        self.value['n'] = int(self.value['n']) + 1
        old_x_bar = self.value['x_bar']
        self.value['x_bar'] = self.value['x_bar'] + ( (value['x'] - self.value['x_bar']) / n )
        self.value['y_bar'] = self.value['y_bar'] + ( (value['y'] - self.value['y_bar']) / n )
        self.value['cov'] = (self.value['cov'] + ((value['y'] - self.value['y_bar']) * (value['x'] - old_x_bar))) / self.value['n']
    
    def __add__(self, other):
        new_value = float(self.value[self.main]) + float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Co-Variance can not be less than zero!") 

    def __sub__(self, other):
        new_value = float(self.value[self.main]) - float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Co-Variance can not be less than zero!")

    def __truediv__(self, other):
        new_value = float(self.value[self.main]) / float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Co-Variance can not be less than zero!")

    def __mul__(self, other):
        new_value = float(self.value[self.main]) * float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Co-Variance can not be less than zero!")
    
# Correlation still to be implemented. Should be Pearson's?
#class Correlation(__strmBase):
#
#    def __init__(self):

def list_of_base(objects, _t):
    """ Transform a dictionary of keys and thetas into a dictionary of keys and
    classes of the corresponding types

    ... note: Perhaps here it is wished to have a distinction between a dict of
    dict of thetas and only a dict of thetas?
    
    :param dict objects: This is typically a dictionary of dicts of thetas
    :param type _t: The class type that is wished to have.
    :returns dict: A dict of dicts with classes _t
    """
    base_list = {}
    for key, obj in objects.items():
        base_list[key] = _t(obj)
    return base_list

# List (of objects)
#class ListOfBase():
#
#    def __init__(self, objects, _t):
#        self.base_list = {}
#        for key, obj in objects:
#            self.base_list[key] = _t(obj)
#        self.size = len(self.base_list)
#    
#    def __iter__(self):
#        self.count = 0
#        return self
#
#    def __next__(self):
#        if self.count == self.size:
#            return StopIteration


