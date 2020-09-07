import os


######### LO DEJO EN gce!!!!!!!!!!!!!!!
template = "CF_default_nlo__TC_vbf_common_os_even__FT_{0[0]}__AR_{0[1]}__LN_gce__L2_{0[2]}__EW_1__LR_{0[3]}__DO_{0[4]}__BN_1__BS_1024__RS_{0[5]}/"
a = []
#a.append(["lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "2p00e-03", "5p00e-05", "0p1"])
#a.append(["lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "6p00e-03", "1p00e-05", "0p05"])
#a.append(["lbn"      ,"lbn_dense:30:default:128_128_128_128:tanh", "2p00e-02", "1p00e-05", "0p0"])
#a.append(["lbn"      ,"lbn_dense:30:extended:128_128_128_128:tanh", "6p00e-03", "1p00e-05", "0p0"])
#a.append(["lbn_light","lbn_dense:30:extended:256_256_256_256:tanh", "6p00e-04", "1p00e-05", "0p0"])
#a.append(["lbn_light","lbn_dense:30:extended:256_256_256_256:tanh", "2p00e-02", "5p00e-05", "0p1"])
#a.append(["lbn_light","lbn_dense:30:extended:256_256_256_256:tanh", "2p00e-03", "5p00e-05", "0p05"])
#a.append(["lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "6p00e-04", "5p00e-05", "0p0"])
#a.append(["lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "6p00e-04", "1p00e-05", "0p05"])
#a.append(['lbn', 'lbn_dense:30:default:128_128_128_128:tanh', '2p00e-02', '5p00e-04', '0p0'])
#a.append(['lbn_light', 'lbn_dense:30:extended:128_128_128_128:tanh', '6p00e-04', '5p00e-05', '0p0'])
#a.append(['lbn_light', 'lbn_dense:30:default:128_128_128_128:tanh', '2p00e-03', '5p00e-05', '0p1'])
#a.append(['lbn_light', 'lbn_dense:30:default:128_128_128_128:tanh', '6p00e-02', '1p00e-05', '0p05'])
#a.append(['lbn_light', 'lbn_dense:30:default:128_128_128_128:tanh', '6p00e-03', '1p00e-05', '0p05'])
a.append(['lbn_light', 'lbn_dense:30:default:128_128_128_128:tanh', '6p00e-03', '1p00e-05', '0p05'])
#folder = "/eos/home-j/jleonhol/hmc/ScanPlot/base_2018_2016_2017/"
#folder = "/eos/home-m/mrieger/hmc/Training/base_2018_2016_2017/"
folder = "/eos/home-j/jleonhol/hmc/Training/base_2018_2016_2017/"
#my_folder = "/eos/home-j/jleonhol/hmc/Training/base_2017_2016_2018/"
my_folder = "/eos/home-j/jleonhol/hmc/Training/base_2016_2017_2018/"



for index, s in enumerate(a):
    print index
        #i = "_".join([str(num) for num in  range(1,11)]) 
    for i in range(1,11):
        b = s + [i]
        #f = folder + template.format(b).replace(":","_") + "cat_vbf_loose/hyperopt1/"
        f = folder + template.format(b).replace(":","_") + "hyperopt1/"
        if not os.path.isdir(f):
            print f, "doesnt exist"
        else:
            if not os.path.isdir(my_folder + template.format(b).replace(":","_")):
                os.mkdir(my_folder + template.format(b).replace(":","_"))
            os.system("cp -r " + f + " " + my_folder + "/" +  template.format(b).replace(":","_"))
