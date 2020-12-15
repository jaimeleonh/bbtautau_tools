import json
import tabulate
import os
from collections import OrderedDict

regions = OrderedDict()
regions["os_iso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau__NO_STR/yields/lep1_pt__qcd__tautau_os_iso.json"
regions["ss_iso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau__NO_STR/yields/lep1_pt__tautau_ss_iso.json"
regions["os_inviso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau__NO_STR/yields/lep1_pt__tautau_os_inviso.json"
regions["ss_inviso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau__NO_STR/yields/lep1_pt__tautau_ss_inviso.json"

summary = []

for region in regions:
    print region
    table = []
    table.append(["process", "value", "error"])
    d = json.load(open(os.path.expandvars(regions[region]), "r"))
    
    if region == "os_iso":
        for regionp in regions:
            if regionp == region: continue
            value = d["n_" + regionp]
            error = d["n_" + regionp + "_error"]
            dec = 1
            while (True):
                if round(value, dec + 1) != 0 and round(error, dec + 1) != 0:
                    value = round(value, dec + 1)
                    error = round(error, dec + 1)
                    break
                if dec == 10:
                    break
                dec += 1
            summary.append([regionp, value, error])
    
    for proc in d["yields"]:
        value = float(d["yields"][proc]["value"])
        error = float(d["yields"][proc]["error"])
        dec = 1
        while (True):
            if round(value, dec + 1) != 0 and round(error, dec + 1) != 0:
                value = round(value, dec + 1)
                error = round(error, dec + 1)
                break
            if dec == 10:
                break
            dec += 1

        table.append([proc, value, error])
    print tabulate.tabulate(table, tablefmt="latex")
        
    print
        
headers = ["Region", "Value", "Error"]
print tabulate.tabulate(summary, tablefmt="latex", headers=headers)
