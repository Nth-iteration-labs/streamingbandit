import numpy as np
#import json
#from scipy.optimize import minimize_scalar

class __strmBase(object):
    
    def __init__(self):
        self.value = False
        self.main = ""
        
    # THIS SHOULD BE IMPLEMENTED IN experiment.set_theta()
	# if isinstance(values, __strmBase):
	#	values = values.get_value()
    def get_value(self):
        return self.value
        
    # We might be able to make generic operators:
    def __add__(self, value):
        self.value[self.main] = int(self.value[self.main]) + int(value)


class Count(__strmBase):
    
    def __init__(self, default={"n":0}):
        self.value = default.copy()
        
    def __add__(self, value):
        self.value["n"] = int(self.value["n"]) + int(value)
        
    # ALL OPERATORS (+,-,*,/) SHOULD BE IMPLEMENTED
    # http://www.python-course.eu/python3_magic_methods.php
    
    def update(self, value=1):
        self.__add__(value)
        
    def increment(self):
        self.value["n"] = int(self.value["n"]) + 1
        

class Mean(Count):
    
    def __init__(self, default={"n":0, "m":0}):
        self.main = "m"
        self.value = default.copy()
        
    def update(self, value):
        self.value['n'] = int(self.value['n']) + 1
        current['m'] = float(self.value['m']) + ( (float(value) - float(self.value['m'])) / self.value['n'])
   
    def get_count(self):
        return self.value["n"]

# Mean
# Variance (Welford's method)
# Proportion (Same as mean, but bounded 0,1 and default = {"n":2, "p":.5})
# Covariance
# Correlation
# List (of objects)