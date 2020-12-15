from subprocess import call
command = ("law run QCDTest3 --feature-names {}    --version qcd_test__new__{}   --category-name {}    --region-name {}_os_iso --SkimCategorization-version prod{} "
    "--MergeCategorizationStats-version prod{} --MergeCategorization-version prod{} --workers 8 --skip-dataset-names hh_vbf_c2v,hh_vbf_1_0_1,hh_ggf_0 --config-name base_{} "
    "--data-config-names {} --EvaluateData-version hyperopt6_prod8 --Training-version hyperopt6 --training-category-name vbf_os --TrainingOutputPlot-cross-evaluation --training-config-name default "
    "--architecture lbn_dense:30:default:0_4:tanh     --feature-tag lbn_light     --l2-norm 1  --learning-rate 1    --dropout-rate 1 --random-seeds 1,2,3,4,5,6,7,8,9,10 "
    "--loss-name bsm --event-weights False")

params = {}
params[2016] = {}
#params[2016]["boosted"] = (8, "lep1_pt")
#params[2016]["resolved_1b"] = (9, "lep1_pt") 
#params[2016]["resolved_2b"] = (8, "lep1_pt") 
params[2016]["vbf"] = (8, "DNNoutSM_kl_1_hh_vbf_sm_c2v_merged_mpp,DNNoutSM_kl_1_hh_ggf_merged_mpp,"
    "DNNoutSM_kl_1_tt_merged_mpp,DNNoutSM_kl_1_tth_merged_mpp,DNNoutSM_kl_1_dy_merged_mpp")
params[2017] = {}
#params[2017]["boosted"] = (9, "lep1_pt") 
#params[2017]["resolved_1b"] = (10, "lep1_pt") 
#params[2017]["resolved_2b"] = (9, "lep1_pt") 
params[2017]["vbf"] = (9, "DNNoutSM_kl_1_hh_vbf_sm_c2v_merged_mpp,DNNoutSM_kl_1_hh_ggf_merged_mpp,"
    "DNNoutSM_kl_1_tt_merged_mpp,DNNoutSM_kl_1_tth_merged_mpp,DNNoutSM_kl_1_dy_merged_mpp")  
params[2018] = {}
#params[2018]["boosted"] = (8, "lep1_pt") 
#params[2018]["resolved_1b"] = (9, "lep1_pt") 
#params[2018]["resolved_2b"] = (8, "lep1_pt") 
params[2018]["vbf"] = (8, "DNNoutSM_kl_1_hh_vbf_sm_c2v_merged_mpp,DNNoutSM_kl_1_hh_ggf_merged_mpp,"
    "DNNoutSM_kl_1_tt_merged_mpp,DNNoutSM_kl_1_tth_merged_mpp,DNNoutSM_kl_1_dy_merged_mpp")

for year in params:
    if year == 2016:
        data_config_names = "base_2017,base_2018"
    elif year == 2017:
        data_config_names = "base_2016,base_2018"
    elif year == 2018:
        data_config_names = "base_2016,base_2017"
    for category in params[year]:
    
        for channel in ["tautau", "mutau", "etau"]:
            print command.format(params[year][category][1], channel, category, channel, params[year][category][0],
                params[year][category][0], params[year][category][0], year, data_config_names)
            rc = call(command.format(params[year][category][1], channel, category, channel, params[year][category][0],
                params[year][category][0], params[year][category][0], year, data_config_names), shell=True)

    
