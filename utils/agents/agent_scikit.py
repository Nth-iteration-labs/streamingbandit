# -*- coding: utf-8 -*-
import numpy as np
import pickle
import json


def skimport(name):
        m = __import__(name)
        for n in name.split(".")[1:]:
            m = getattr(m, n)
        return m



#>>> import numpy as np
#>>> from sklearn import linear_model
#>>> n_samples, n_features = 10, 5
#>>> np.random.seed(0)
#>>> y = np.random.randn(n_samples)
#>>> X = np.random.randn(n_samples, n_features)
#>>> clf = linear_model.SGDRegressor()
#>>> clf.fit(X, y)

# Example usage of SciKitLearn
skClass = "linear_model"
skM = skimport("sklearn."+skClass)
m1 = getattr(skM, "SGDRegressor")()

#m1 = skM.SGDRegressor() 
#m1 = skimport("sklearn.linear_model.SGDRegressor")

n_samples, n_features = 10, 2
np.random.seed(0)
y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)
print(X)
#
## fit the model
print(m1.coef_) 
m1.fit(X, y)
print(m1.coef_)
#
## Dump the model
s = pickle.dumps(m1)
d = {"picklestr":s}
print(d)    # This can be stored in MongoDB


# Load the model:
m2 = pickle.loads(d["picklestr"])
print(m2.coef_)

# Predict a new value based on a new feature vector:
print(m2.predict(X[0:1]))

# Incremental fit using partial_fit functions
m2.partial_fit(np.array([[1,20]]), np.array([1000]))
print(m2.coef_)
print(m2.predict(np.array([[1,20]])))