from subprocess import call
from math import sqrt
from collections import OrderedDict

command = ("law run FeaturePlotQCDTest --feature-names {}    --version qcd_test__btag__{}   --category-name {}    --region-name {}_os_iso --SkimCategorization-version prod{} "
    "--MergeCategorizationStats-version prod{} --MergeCategorization-version prod{} --workers 9 --skip-dataset-names hh_vbf_c2v,hh_vbf_1_0_1,hh_ggf_0 --config-name base_{} "
    "--data-config-names {} --EvaluateData-version hyperopt6_prod8 --Training-version hyperopt6 --training-category-name vbf_os --TrainingOutputPlot-cross-evaluation --training-config-name default "
    "--architecture lbn_dense:30:default:0_4:tanh     --feature-tag lbn_light     --l2-norm 1  --learning-rate 1    --dropout-rate 1 --random-seeds 1,2,3,4,5,6,7,8,9,10 "
    "--loss-name bsm --event-weights False")
    
def make_red(string):
    return "\\textcolor{red}{" + string + "}"
def make_green(string):
    return "\\textcolor{mynicegreen}{" + string + "}"
def make_blue(string):
    return "\\textcolor{blue}{" + string + "}"

params = OrderedDict()
params[2016] = OrderedDict() 
params[2016]["boosted"] = (8, "lep1_pt")
params[2016]["boosted_nobtag"] = (8, "lep1_pt")
params[2016]["boosted_nomcut"] = (8, "lep1_pt")
params[2016]["resolved_1b"] = (9, "lep1_pt") 
params[2016]["resolved_2b"] = (8, "lep1_pt") 
params[2016]["vbf"] = (8, "DNNoutSM_kl_1_hh_vbf_sm_c2v_merged_mpp,DNNoutSM_kl_1_hh_ggf_merged_mpp,"
    "DNNoutSM_kl_1_tt_merged_mpp,DNNoutSM_kl_1_tth_merged_mpp,DNNoutSM_kl_1_dy_merged_mpp")
params[2017] = OrderedDict()
params[2017]["boosted"] = (9, "lep1_pt") 
params[2017]["boosted_nobtag"] = (9, "lep1_pt")
params[2017]["boosted_nomcut"] = (9, "lep1_pt")
params[2017]["resolved_1b"] = (10, "lep1_pt") 
params[2017]["resolved_2b"] = (9, "lep1_pt") 
params[2017]["vbf"] = (9, "DNNoutSM_kl_1_hh_vbf_sm_c2v_merged_mpp,DNNoutSM_kl_1_hh_ggf_merged_mpp,"
    "DNNoutSM_kl_1_tt_merged_mpp,DNNoutSM_kl_1_tth_merged_mpp,DNNoutSM_kl_1_dy_merged_mpp")  
params[2018] = OrderedDict()
params[2018]["boosted"] = (8, "lep1_pt") 
params[2018]["boosted_nobtag"] = (8, "lep1_pt")
params[2018]["boosted_nomcut"] = (8, "lep1_pt")
params[2018]["resolved_1b"] = (9, "lep1_pt") 
params[2018]["resolved_2b"] = (8, "lep1_pt") 
params[2018]["vbf"] = (8, "DNNoutSM_kl_1_hh_vbf_sm_c2v_merged_mpp,DNNoutSM_kl_1_hh_ggf_merged_mpp,"
    "DNNoutSM_kl_1_tt_merged_mpp,DNNoutSM_kl_1_tth_merged_mpp,DNNoutSM_kl_1_dy_merged_mpp")

version = "__btag"

txtname = "/eos/user/j/jleonhol/hmc/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + version + "__{}/qcd_inviso__{}__{}.txt"
ss_iso_name = "/eos/user/j/jleonhol/hmc/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + version + "__{}/n_ss_iso__{}__{}.txt"
ss_inviso_name = "/eos/user/j/jleonhol/hmc/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + version + "__{}/n_ss_inviso__{}__{}.txt"
os_inviso_name = "/eos/user/j/jleonhol/hmc/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + version + "__{}/n_os_inviso__{}__{}.txt"

stuff = OrderedDict() 
for year in params:
    stuff[year] = OrderedDict()
    for category in params[year]:
        stuff[year][category] = OrderedDict()
        for channel in ["tautau", "mutau", "etau"]:
            stuff[year][category][channel] = OrderedDict()
            for feature in params[year][category][1].split(","):
                stuff[year][category][channel][feature] = OrderedDict()
ss_iso = OrderedDict() 
ss_inviso = OrderedDict()
os_inviso = OrderedDict()
for year in params:
    ss_iso[year] = OrderedDict()
    ss_inviso[year] = OrderedDict()
    os_inviso[year] = OrderedDict()
    for category in params[year]:
        ss_iso[year][category] = OrderedDict()
        ss_inviso[year][category] = OrderedDict()
        os_inviso[year][category] = OrderedDict()            
        for feature in params[year][category][1].split(","):
            ss_iso[year][category][feature] = OrderedDict()
            ss_inviso[year][category][feature] = OrderedDict()
            os_inviso[year][category][feature] = OrderedDict()         

def get_year(year, feature):
    years = ["2016", "2017", "2018"]
    if "DNN" not in feature or True:
        return year
    # else:
        # return "_".join([str(year)] + [y for y in years if y != str(year)])


skip = (False and "remove" not in command)
for year in params:
    for category in params[year]:
        for channel in ["tautau", "mutau", "etau"]:
            if not skip:
                if year == 2016:
                    data_config_names = "base_2017,base_2018"
                elif year == 2017:
                    data_config_names = "base_2016,base_2018"
                elif year == 2018:
                    data_config_names = "base_2016,base_2017"
                rc = call(command.format(params[year][category][1], channel, category, channel,
                    params[year][category][0], params[year][category][0], params[year][category][0],
                    year, data_config_names), shell=True)
            if "remove" not in command:
                for feature in params[year][category][1].split(","):
                    name = txtname.format(get_year(year, feature), category, channel, channel, feature)
                    with open(name) as f:
                        lines = f.readlines()
                        for l in lines:
                            values = l.strip().split(" ")
                            # print name, values
                            stuff[year][category][channel][feature][values[0]] = (values[1],
                                values[2])
                    name = ss_iso_name.format(get_year(year, feature), category, channel, channel, feature)
                    with open(name) as f:
                        lines = f.readlines()
                        if lines: l = lines[0]
                        values = l.strip().split(" ")
                        ss_iso[year][category][feature][channel] = (float(values[1]),
                            float(values[2]))

                    name = ss_inviso_name.format(get_year(year, feature), category, channel, channel, feature)
                    with open(name) as f:
                        lines = f.readlines()
                        if lines: l = lines[0]
                        values = l.strip().split(" ")
                        ss_inviso[year][category][feature][channel] = (float(values[0]),
                            float(values[1]))

                    name = os_inviso_name.format(get_year(year, feature), category, channel, channel, feature)
                    with open(name) as f:
                        lines = f.readlines()
                        if lines: l = lines[0]
                        values = l.strip().split(" ")
                        os_inviso[year][category][feature][channel] = (float(values[0]),
                            float(values[1]))

def get_param(tup):
    if isinstance(tup[1], str):
        num = tup[1].split("*")
    else:
        num = [tup[1]]
    num_of_zeros = len(num) - 1
    value = float(tup[0])
    error = float(num[0])
    if value == 0.:
        return "0", num_of_zeros
    else:
       my_str = "${:.3f} \pm {:.3f}$ $({:>2.1f}\\%)$".format(value, error, 100 * error/value)
       return my_str, num_of_zeros

if "remove" not in command:
    for year in stuff:
        print "********* {} *********".format(year)
        for category in stuff[year]:
            for feature in params[year][category][1].split(","):
                for i, channel in enumerate(["tautau", "mutau", "etau"]):
                    my_chan = "$" + channel.replace("tau", "\\tau").replace("mu", "\\mu") + "$"
                    my_cat = category.replace("_", "\\_") if i == 1 else ""
                    my_feature = "" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                    this_st = stuff[year][category][channel][feature]
                    
                    vvl_m_str, num_of_zeros = get_param(this_st["vvl_m"])
                    mean_str, _ = get_param(this_st["Mean"])
                    if mean_str == "0":
                        mean_str = "-"
                        num_of_zeros = 0
                    fit_str, _ = get_param(this_st["Fit"])
                    # print fit_str
                    if fit_str == "0":
                        fit_str = "-"

                    vvl_m_val = float(this_st["vvl_m"][0])
                    vvl_m_error = float(this_st["vvl_m"][1].split("*")[0])
                    mean_val = float(this_st["Mean"][0])
                    
                    if mean_str != "-":
                        if (vvl_m_val - vvl_m_error > mean_val or vvl_m_val + vvl_m_error < mean_val):
                            vvl_m_str = make_red(vvl_m_str)

                    print "{:<15} &  {:<20} &{:<6} & {}{} & {} & {}\\\\".format(
                        my_cat, my_feature, my_chan, vvl_m_str, "*" * num_of_zeros, mean_str, fit_str)
                print "\\hline"

    print
    print 
    
    # for year in ss_iso:
        # print "********* {} *********".format(year)
        # for category in ss_iso[year]:
            # for feature in params[year][category][1].split(","):
                # for i, channel in enumerate(["tautau", "mutau", "etau"]):
                    # my_chan = "$" + channel.replace("tau", "\\tau").replace("mu", "\\mu") + "$"
                    # my_cat = category.replace("_", "\\_") if i == 1 else ""
                    # my_str = (
                        # "0" if stuff[year][category][channel]["vvl_m"] == 0
                        # else "${:<8.3f} \pm {:<8.3f}$ $({:>2.1f}\\%)$".format(
                            # ss_iso[year][category][channel][0], ss_iso[year][category][channel][1], 
                            # 100 * ss_iso[year][category][channel][1] / ss_iso[year][category][channel][0])
                    # )
                    # print "{:<15} & {:<10} & {}\\\\".format(
                        # my_cat, my_chan, my_str)
                # print "\\hline"

    # print
    # print 

    print "******************** lnN ***********************"


    year_string = "{:<15} & {:<20} & {:<10} ".format(" ", " ", " ")
    for year in ss_inviso:
        year_string += "& {:<5} ".format(year)
      
    print year_string + "\\\\"

    for year in ss_inviso:
        if len(ss_inviso[year].keys()) > 0:
            first_year = year
            break

    def rel_error(value):
        return value[1] / value[0] if value[0] != 0 else 0

    for category in ss_inviso[first_year]:
        for feature in params[first_year][category][1].split(","):
            for i, channel in enumerate(["tautau", "mutau", "etau"]):
                my_cat = category.replace("_", "\\_") if i == 1 else ""
                my_chan = "$" + channel.replace("tau", "\\tau").replace("mu", "\\mu") + "$"
                my_str = ""
                my_feature = "------" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                my_feature = "" if i != 1 else my_feature
                for year in ss_inviso:
                    if category not in ss_inviso[year].keys():
                        my_str += "& - "
                    else:
                        if ss_iso[year][category][feature][channel][0] - ss_iso[year][category][feature][channel][1] > 0\
                                and ss_inviso[year][category][feature][channel][0] - ss_inviso[year][category][feature][channel][1] > 0:
                            # lnN = ((ss_iso[year][category][channel][0] / ss_inviso[year][category][channel][0]) * 
                            lnN = sqrt(rel_error(ss_inviso[year][category][feature][channel])**2 +
                                rel_error(ss_iso[year][category][feature][channel])**2)
                        else:
                            lnN = -1
                        my_str += (
                            "& {:<5} ".format("$-$") if float(stuff[year][category][channel][feature]["vvl_m"][0]) == 0
                            else "& {:<5.3f} ".format(1 + lnN)
                        )
                print "{:<15} & {:<20} & {:<10} {}\\\\".format(
                    my_cat, my_feature, my_chan, my_str)
            print "\\hline"
    print
    
    
    print "*" * 20
    print "{:^20}".format("QCD diagnosis")
    print "*" * 20
   
    final_table = []

    def redondear(value, error):
        dec = 1
        while (True):
            if round(value, dec + 1) != 0 and round(error, dec + 1) != 0:
                value = round(value, dec + 1)
                error = round(error, dec + 1)
                break
            if dec == 10:
                break
            dec += 1
        return value, error

    def is_compatible(tup):
        if tup[0] - tup[1] < 0:
            return True
        return False

    for year in ss_iso:
        print "********* {} *********".format(year)
        for category in ss_iso[year]:
            for feature in params[year][category][1].split(","):
                for i, channel in enumerate(["tautau", "mutau", "etau"]):
                    my_chan = "$" + channel.replace("tau", "\\tau").replace("mu", "\\mu") + "$"
                    my_cat = category.replace("_", "\\_") if i == 1 else ""
                    my_feature = "-----" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                    my_feature = "" if i != 1 else my_feature

                    if category not in ss_inviso[year].keys():
                        my_str = "& - & - & -"
                    else:
                        my_str = ""
                        is_bad = any([is_compatible(region[year][category][feature][channel])
                            for region in [ss_iso, os_inviso, ss_inviso]])
                        for region in [ss_iso, os_inviso, ss_inviso]:
                            value = region[year][category][feature][channel][0]
                            error = region[year][category][feature][channel][1]
                            value, error = redondear(value, error)                            
                            val_err = "${} \pm {}$".format(value, error)
                            if value - error <= 0:
                                val_err = make_red(val_err)
                            if not is_bad:
                                val_err = make_green(val_err)
                            my_str += "& {} ".format(val_err)
                    print "{:<15} & {:<20} & {:<10} {}\\\\".format(
                        my_cat, my_feature, my_chan, my_str)
            print "\\hline"



    # print 
    # print
    # print year_string + "\\\\\\hline"
    # for category in ss_inviso[first_year]:
        # for i, channel in enumerate(["tautau", "mutau", "etau"]):
            # my_chan = "$" + channel.replace("tau", "\\tau").replace("mu", "\\mu") + "$"
            # my_cat = category.replace("_", "\\_") if i == 1 else ""
            # my_str = ""
            # for year in ss_inviso:
                # if category not in ss_inviso[year].keys():
                    # my_str += "& - "
                # else:
                    # if (not is_compatible(ss_iso[year][category][channel]) and not is_compatible(os_inviso[year][category][channel])
                            # and not is_compatible(ss_inviso[year][category][channel])):
                        # value = ss_iso[year][category][channel][0] * os_inviso[year][category][channel][0] / ss_inviso[year][category][channel][0]
                        # error = value * sqrt(sum([(region[year][category][channel][1] / region[year][category][channel][0]) ** 2
                            # for region in [ss_iso, os_inviso, ss_inviso]]))
                        # value, error = redondear(value, error)
                    # my_str += (
                        # "& {:^5} ".format("$-$") if stuff[year][category][channel]["vvl_m"][0] == 0
                        # else "& $ {} \pm {}$ $({:>2.1f}\\%)$".format(str(value), str(error), error/value)
                    # )
            # print "{:<15} & {:<10} {:<20}\\\\".format(
                # my_cat, my_chan, my_str)
        # print "\\hline"
    # print
