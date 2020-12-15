from subprocess import call
command = ("law run QCDTest2 --FeaturePlot-feature-names {}    --version qcd_test__new__{}   --category-name {}    --region-name {}_os_iso --SkimCategorization-version prod{} "
    "--MergeCategorizationStats-version prod{} --MergeCategorization-version prod{} --workers 8 --skip-dataset-names hh_vbf_c2v,hh_vbf_1_0_1,hh_ggf_0 --config-name base_{}")
params = {}
params[2016] = {}
params[2016]["resolved_1b_inv"] = 8
params[2016]["resolved_1b_inv_b"] = 9 
params[2017] = {}
params[2017]["resolved_1b_inv"] = 9
params[2017]["resolved_1b_inv_b"] = 10
params[2018] = {}
params[2018]["resolved_1b_inv"] = 8
params[2018]["resolved_1b_inv_b"] = 9

#feature_names = ["vbfjet1_eta"]
feature_names = ["lep1_eta,vbfjet1_eta", "lep1_eta", "vbfjet1_eta"]

for year in params:
    for category in params[year]:
        for channel in ["tautau", "mutau", "etau"]:
            for feature in feature_names:
                rc = call(command.format(feature, channel, category, channel, params[year][category],
                    params[year][category], params[year][category], year), shell=True)

    
