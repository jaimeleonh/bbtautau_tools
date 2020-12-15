import os
config = "base_2016"

marcel = "/eos/user/m/mrieger/hmc/MergeShards/{}/".format(config)
jaime = "/eos/user/j/jleonhol/hmc/MergeShards/{}/".format(config)




features = os.listdir(marcel)
for feature in features:
    cmd = "cp -r {}{}/cat_vbf_common_os_even/ {}{}/".format(marcel, feature, jaime, feature)
    print cmd
    os.system(cmd)
