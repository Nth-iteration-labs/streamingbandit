# -*- coding: utf-8 -*-
import libs.base as base
import libs.scikit as skl
X = self.context[""] 
model = skl.Model(value = self.get_theta(), "linear_model", "SGDRegressor")

# Should be nested in some for loop or something for the multiple possible actions
self.action = model.predict(X, y)



