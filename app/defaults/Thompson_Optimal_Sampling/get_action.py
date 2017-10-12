import libs.thompson as thmp
varList = thmp.ThompsonVarList(self.get_theta(key="treatment"), ["control","treatment"])
self.action["treatment"] = varList.experimentThompson()
