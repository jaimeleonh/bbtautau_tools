import os, json, sys


years = ["2016_2017_2018", "2017_2016_2018", "2018_2016_2017"]

foldername = "/eos/user/j/jleonhol/hmc/BinningOptimization/base_{}/CF_default__TC_vbf_common_os_even__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_gce__L2_6p00e-03__EW_1__LR_1p00e-05__DO_0p05__BN_1__BS_1024__RS_1_2_3_4_5_6_7_8_9_10/cat_vbf_loose/opt/"


for year in years:
    filenames = {"tautau":[], "etau":[], "mutau":[]}
    folder = foldername.format(year)
    for f in os.listdir(folder):
        stuff = f.split("__")
        channel = stuff[-1].split("_")[0]
        if "mpp" not in stuff[1]: continue
        feature = stuff[1].split("_")
        end = feature.index("merged")
        feature = "_".join(stuff[1].split("_")[1:end])
        filenames[channel].append((feature, folder + f))
       

    for channel in filenames:
        print "\n#############", year.split("_")[0], channel, "#############\n"
        for filename in filenames[channel]:
            d = json.load(open(os.path.expandvars(filename[1]), "r"))
            print "mdnn__v2__kl1_c2v1_c31__{}  = ".format(filename[0]),
            for i, a in enumerate(d):
                c = "{}".format(a)
                if i < len(d) - 1: c+= ","
                print c,
            print ""
