import numpy as np
import random
#import json
#from scipy.optimize import minimize_scalar

class __strmBase(object):
    """ A streamingbandit base class. Use this skeleton to implement
        classes that represent online/sequential variants of estimators.
        
    .. note:: Upon writing a new class, make sure that every function of this \
    skeleton is implemented correctly for that type of estimator.
    """

    def __init__(self):
        """ Construct a new strmBase object.
        """
        self.value = False
        self.main = ''
        
    def get_value(self):
        """ Get the main value for the estimator. For example, for the \
        estimator Mean this would be the mean itself.
        """
        return float(self.value[self.main])

    def get_dict(self):
        """ Return all the vars that are needed to do an online \ 
        estimation in a dictionary.
        """
        return self.value
        
    def __add__(self, other):
        """ Override the arithmetic + function.
        """
        self.value[self.main] = int(self.value[self.main]) + int(other)

    def __sub__(self, other):
        """ Override the arithmetic - function.
        """
        self.value[self.main] = int(self.value[self.main]) - int(other)

    def __truediv__(self, other):
        """ Override the arithmetic / function.
        """
        self.value[self.main] = float(self.value[self.main]) / float(other)

    def __mul__(self, other):
        """ Override the arithmetic * function.
        """
        self.value[self.main] = float(self.value[self.main]) * float(other)


class Count(__strmBase):
    """ Class to represent a counter using an online estimator.

    :var dict default: A dictionary that consists of the counter n. Leave \
    empty to start a new counter.
    """

    def __init__(self, default):
        self.main = 'n'
        if default == {}:
            self.value = {'n':0}
        else:
            self.value = default.copy()
    
    def update(self, value=1):
        """ Adds value to the counter.
        """
        self.__add__(value)
        
    def increment(self):
        """ Update the counter with value 1.
        """
        self.value['n'] = int(self.value['n']) + 1
        

class Mean(Count):
    """ Class to represent a mean using an online estimator.
    
    :var dict default: A dictionary that consists of a counter n and mean \
    m. Leave empty to start a new mean.
    """

    def __init__(self, default):
        self.main = 'm'
        if default == {}:
            self.value = {'n':0, 'm':0}
        else:
            self.value = default.copy()
        
    def update(self, value):
        """ Adds value to the mean.

        :param int value: The value of x to update the mean.
        """
        self.value['n'] = int(self.value['n']) + 1
        self.value['m'] = float(self.value['m']) + ( (float(value) - float(self.value['m'])) / float(self.value['n']))
   
    def get_count(self):
        """ Returns the counter of the mean object.
        """
        return int(self.value['n'])


class Variance(__strmBase):
    """ Class to represent a variance using an online estimator.

    :var dict default: A dictionary that consists of a counter n, mean \
    x_bar, standard deviation s and variance v. Leave empty to start a new \
    variance.
    """

    def __init__(self, default):
        self.main = 'v'
        if default == {}:
            self.value = {'n':0, 'x_bar':0, 's':0, 'v':0}
        else:
            self.value = default.copy()

    def update(self, value):
        """ Adds value to the variance.

        :param int value: The value used for updating.
        """
        d = float(value) - float(self.value['x_bar'])
        self.value['n'] = int(self.value['n']) + 1
        self.value['x_bar'] = float(self.value['x_bar']) + ((float(value) - float(self.value['x_bar'])) / (int(self.value['n'])))
        self.value['s'] = float(self.value['s']) + ( d * (float(value) - float(self.value['x_bar'])) )
        if self.value['n'] >= 2:
            self.value['v'] = float(self.value['s'])/(int(self.value['n']) - 1)

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
    """ Class to represent a proportion using an online estimator.

    :var dict default: A dictionary that consists of a counter n, and \
    proportion p. Leave empty to start a new proportion.
    """

    def __init__(self,default):
        self.main = 'p'
        if default == {}:
            self.value = {'p': 0, 'n': 0}
        else:
            self.value = default.copy()

    def update(self, value):
        """ Adds value to the proportion. 

        :param int value: A value 0 or 1.
        """
        self.value['n'] = int(self.value['n']) + 1
        self.value['p'] = float(self.value['p']) + ( (value - float(self.value['p'])) / int(self.value['n']))

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
    """ Class to represent a covariance using an online estimator.

    :var dict default: A dictionary that consists of a counter n, mean \
            for x x_bar, mean for y y_bar and covariance cov. Leave empty to \
            start a new covariance.
    """

    def __init__(self,default):
        self.main = 'cov'
        if default == {}:
            self.value = {'n':0, 'x_bar':0, 'y_bar':0, 'cov':0}
        else:
            self.value = default.copy()

    def update(self, value):
        """ Adds value to covariance. 

        :param dict value: A dict of ints of x and y.
        """
        # Value must be a dict of x and y as
        # {'x' : 0, 'y' : 0} since we compute covariance of two datapoints
        self.value['n'] = int(self.value['n']) + 1
        self.value['x_bar'] = float(self.value['x_bar']) + ( (float(value['x']) - float(self.value['x_bar'])) / int(self.value['n']) )
        self.value['y_bar'] = float(self.value['y_bar']) + ( (float(value['y']) - float(self.value['y_bar'])) / int(self.value['n']) )
        self.value['cov'] = float(self.value['cov']) + ((float(value['y']) - float(self.value['y_bar'])) * (float(value['x']) - float(self.value['x_bar']))) 
   
    def __add__(self, other):
        new_value = float(self.value[self.main]) + float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Covariance can not be less than zero!") 

    def __sub__(self, other):
        new_value = float(self.value[self.main]) - float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Covariance can not be less than zero!")

    def __truediv__(self, other):
        new_value = float(self.value[self.main]) / float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Covariance can not be less than zero!")

    def __mul__(self, other):
        new_value = float(self.value[self.main]) * float(other)
        if new_value >= 0:
            self.value[self.main] = new_value
        else:
            raise ValueError("Covariance can not be less than zero!")
    
class Correlation(__strmBase):
    """ Class to represent a correlation using an online estimator.

    :var dict default: A dictionary that consists of a counter n, mean \
            for x x_bar, mean for y y_bar, standard deviation for x x_s, \
            standard deviation for y y_s, variance for x x_v, variance for y \
            y_v, covariance cov and correlation c. Leave empty to start a new correlation.
    """

    def __init__(self, default):
        self.main = 'c'
        if default == {}:
            self.value = {'n':0, 'x_bar':0, 'y_bar':0, 'x_s':0, 'y_s':0, 'x_v':0, 'y_v':0, 'cov':0, 'c':0}
        else:
            self.value = default.copy()

    def update(self, value):
        """ Adds value to correlation.
        
        :param dict value: A dict of ints of x and y.
        """
        self.value['n'] = int(self.value['n']) + 1
        d_x = float(value['x']) - float(self.value['x_bar'])
        d_y = float(value['y']) - float(self.value['y_bar'])
        self.value['x_bar'] = float(self.value['x_bar']) + ((float(value['x']) - float(self.value['x_bar'])) / int(self.value['n']))
        self.value['y_bar'] = float(self.value['y_bar']) + ((float(value['y']) - float(self.value['y_bar'])) / int(self.value['n']))
        self.value['x_s'] = float(self.value['x_s']) + (d_x * (float(value['x']) - float(self.value['x_bar'])))
        self.value['y_s'] = float(self.value['y_s']) + (d_y * (float(value['y']) - self.value['y_bar']))
        self.value['cov'] = float(self.value['cov']) + ((float(value['y']) - float(self.value['y_bar'])) * (float(value['x']) - float(self.value['x_bar'])))
        if int(self.value['n']) >= 2:
            self.value['x_v'] = float(self.value['x_s']) / (int(self.value['n'] - 1))
            self.value['y_v'] = float(self.value['y_s']) / (int(self.value['n'] - 1))
            self.value['c'] = float(self.value['cov']) / (np.sqrt(float(self.value['x_v'])) * np.sqrt(float(self.value['y_v'])))

    def __add__(self, other):
        new_value = float(self.value[self.main]) + float(other)
        if -1 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Correlation should be between -1 and +1!") 

    def __sub__(self, other):
        new_value = float(self.value[self.main]) - float(other)
        if -1 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Correlation should be between -1 and +1!")

    def __truediv__(self, other):
        new_value = float(self.value[self.main]) / float(other)
        if -1 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Correlation should be between -1 and +1!")

    def __mul__(self, other):
        new_value = float(self.value[self.main]) * float(other)
        if -1 <= new_value <= 1:
            self.value[self.main] = new_value
        else:
            raise ValueError("Correlation should be between -1 and +1!")

class List():
    """ Class to represent a list of Base classes. Here you can store multiple \
    Base classes to simplify your AB test and whatnot.

    :var dict objects: A dict of dicts with the objects in dictionary \
            form - so not a class instance!
    :var type _t: The type of Base class (e.g. Proportion, Count).
    :var list value_names: The different value names that are in the \
            objects dict. This is used for e.g. random picks.
    """

    def __init__(self, objects, _t, value_names):
        self.base_list = {}
        self.value_names = value_names
        self.num_values = len(self.value_names)
        if objects == {}:
            for value_name in self.value_names:
                self.base_list[value_name] = _t(default={})
        elif len(objects) < len(self.value_names):
            for key, obj in objects.items():
                self.base_list[key] = _t(default=obj)
            for val in self.value_names:
                if val not in self.base_list:
                    self.base_list[val] = _t(default={})
        else:
            for key, obj in objects.items():
                self.base_list[key] = _t(default=obj)
        self.size = len(self.base_list)
    
    def get_dict(self):
        """ Returns each Base class in the objects as a dict in a dict.
        """
        dict_list = {}
        for key, val in self.base_list.items():
            dict_list[key] = val.get_dict()
        return dict_list

    def max(self):
        """ Finds the max of the main value of a Base class.
        If no max is available yet (because the values are empty), it will return a random max.
        """
        max_val = 0
        max_key = ""
        for key, value in self.base_list.items():
            if value.get_value() > max_val:
                max_key = key
                max_val = value.get_value()
        if max_key == "":
            max_key = self.random()
        return max_key

    def count(self):
        """ Checks if the Base class has a counter. If that's the case, it will
        add all the counters and return the total count.
        """
        count = 0
        for key, value in self.base_list.items():
            values = value.get_dict()
            if 'n' not in values:
                break
            count = count + int(values['n'])
        return count

    def random(self):
        """ Return a random choice from the value_names list.
        """
        return random.choice(self.value_names)
