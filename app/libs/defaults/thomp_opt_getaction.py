import libs.thompson as thmp
varList = thmp.ThompsonVarList(self.get_theta(key="Treatment"), ["1","2"])
self.action["Treatment"] = varList.experimentThompson()
