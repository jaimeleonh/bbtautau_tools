import csv, os
def import_hyperparams():
    with open('hyperparams.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        hyperparams = []
        for i, row in enumerate(spamreader):
            if i == 0: 
                keys = row
            else:
                hyperparams.append(dict(zip(keys, row)))
    return hyperparams

def sort_params(hyperparams, param_to_sort="hh_vbf",
        params_to_show=["Id", "hh_vbf", "hh_ggf", "tt_fh", "dy"],
        skip_seeds=True, number_to_show=30):

    hyperparams.sort(key=lambda x:x[param_to_sort], reverse=True)
    counter = 0
    stuff = []
    for i in hyperparams:
        if skip_seeds and i["Seed"] != "1":
            continue
        params = []
        for param in params_to_show:
            params.append(i[param])
            print "{}:{:>15} | ".format(param, i[param]),
        if param_to_sort not in params_to_show:
            print "({}:{})".format(param_to_sort, i[param_to_sort])
        print ""
        stuff.append(params)
        counter += 1
        if counter == number_to_show:
            break
    return stuff

hyperparams = import_hyperparams()
stuff = sort_params(hyperparams)
#stuff = sort_params(hyperparams, params_to_show=["Features", "Architecture", "L2 norm", "Learning rate", "Dropout"])
#for i in stuff:
#    print i
# a.append(["lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "6p00e-04", "1p00e-05", "0p05"])
#sort_params(hyperparams)
