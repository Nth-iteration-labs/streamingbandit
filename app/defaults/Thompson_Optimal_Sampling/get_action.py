import libs.thompson as thmp
varList = thmp.ThompsonVarList(self.get_theta(key="treatment"), ["1","2"])
self.action["treatment"] = varList.experimentThompson()
