# -*- coding: utf-8 -*-
import libs.base as base
import libs.scikit as skl
X = self.context[""] 
y = self.reward[""]
model = skl.Model(value = self.get_theta(), "linear_model", "SGDRegressor")
model.update(X, y)
self.set_theta(model)
