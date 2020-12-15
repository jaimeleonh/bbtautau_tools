# coding: utf-8
import os
from collections import OrderedDict
from copy_to_eos import copy_index

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Some options')
    parser.add_argument('-y', '--year', type=int, default = 2016)
    parser.add_argument('-c', '--copy', action='store_false', default = True)
    parser.add_argument('-r', '--ratio', action='store_true', default = False)
    parser.add_argument('-d', '--delete', action='store_true', default = False)
    parser.add_argument('-ch', '--channel', dest='channel', default = "tautau")
    return parser.parse_args()

def combine_parser(file, conf_level="50.0"):
    import os
    with open(os.path.expandvars(file), "r") as f:
        lines = f.readlines()
        for line in lines:
            if str(conf_level)+"%" in line:
                return float(line.split(" ")[-1][0:-1])
    return -1.


def scan_plot(plots, cls, legends, min_x=-999, max_x=999, min_y=-999, max_y=999, x_title="", y_title="",
        text=None, x_log=False, y_log=False, do_ratio=False, step=1, pdf_output_path=""):
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    ax = plt.subplot()

    colors =["b", "r", "g", "c", "m", "y", "k"] 
    markers = ["o","s","^"]
    #markers = ["o"]

    filenames = []

    def sort_by_x(point):
        return point[0]
    if do_ratio:
        ratio_values = [(float(x), y) for (x, y) in plots[0]]
        ratio_values.sort(key=sort_by_x)

    i = -1
    for plot, legend in zip(plots, legends):
        i += 1
        values = [(float(x), y) for (x, y) in plot]
        values.sort(key=sort_by_x)
        if do_ratio:
            values = [(float(x), y / y_r) for ((x, y), (x_r, y_r)) in zip(values, ratio_values)]
        if i >= len(colors) * 2:
            i = 0
            markers = ["^", "v"]
        #color = colors[i / 3]
        #color = colors[i / 2]
        color = colors[(i / step) % len(colors)]
        marker = markers[i % step]
        #marker = markers[i % 2]
        #marker = markers[0]

        plt.plot([x[0] for x in values], [x[1] for x in values], color=color, marker=marker, label=legend)
    
    
    if cls:
        values = [(float(a[0]), float(a[1][0]), float(a[1][1])) for a in cls["68% expected"]]
        
        def sort_by_x(point):
            return point[0]
        values.sort(key=sort_by_x)
        
        plt.fill_between([x[0] for x in values], [x[2] for x in values], [x[1] for x in values],
                         color="g", alpha=.5)
        
        values = [ (float(a[0]), float(a[1][0]), float(a[1][1])) for a in cls["95% expected"]]
        values.sort(key=sort_by_x)
        plt.fill_between([x[0] for x in values], [x[2] for x in values], [x[1] for x in values],
                         color="y", alpha=.5)

    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.grid(True)
    if text:
        x_text = 0.1
        y_text = 0.9

        for t in text:
            plt.text(x_text, y_text, t, transform=ax.transAxes)
            y_text -= 0.05

    xlim = ax.get_xlim()
    min_x = xlim[0] if min_x == -999 else min_x
    max_x = xlim[1] if max_x == 999 else max_x
    ax.set_xlim(min_x, max_x)

    ylim = ax.get_ylim()
    min_y = ylim[0] if min_y == -999 else min_y
    max_y = ylim[1] if max_y == 999 else max_y
    ax.set_ylim(min_y, max_y)

    plt.legend(bbox_to_anchor=(1.13, 1.13))

    if y_log:
        plt.yscale('log')
    if x_log:
        plt.xscale('log')

    plt.savefig(pdf_output_path)
    plt.close('all')
    return pdf_output_path

def dump_francesco(values=None, folder="/eos/user/f/fbrivio/Hhh_1718/datacards_VBFtest/cards_TauTauHHbtagVBFnodeVBFloose/comb_cat/", filename="dump_francesco.json"):
    import json, os
    from combine_tools import get_theo_xs
    from collections import OrderedDict
    outfile = folder + "/out_Asym_{}_noTH.log"
    runfile = folder + "/runJob_Asym_{}.sh"
    
    a = 1 
    list_of_files = os.listdir(folder)
    limits = []
    while (a != -1):
        run = runfile.format(a)
        if os.path.isfile(run):
            print runfile.format(a)
            with open (os.path.expandvars(run), "r") as run_f:
                lines = run_f.readlines()
                for l in lines: 
                    if "C2V" in l:
                        c2v = float(l.split("C2V")[1].split(" ")[0][1:])
                        break
            if not values or c2v in values:
                limit = combine_parser(outfile.format(a))
                limit *= 1000 * get_theo_xs(c2v=c2v)
                limits.append((c2v, limit))
                             
            a += 1 
        else: 
            a = -1
    limits.sort(key=lambda x:x[0])
    json_dict = OrderedDict()
    json_dict["values"] = OrderedDict(limits)
    with open(os.path.expandvars(filename), "w+") as f:
        json.dump(json_dict, f, indent=4)



def plot_scans(filenames, legends, output_name="comparison{}.pdf", logy=False, ratio=False, do_ratio=False, text=None, step=1):
    import os, json, sys
    plots = []
    for i, filename in enumerate(filenames):
        d = json.load(open(os.path.expandvars(filename), "r"))
        plots.append(list(zip(d["values"].keys(), d["values"].values())))
        if i == 0 and True:
            cls = OrderedDict([
                    ("68% expected", d["conf_intervals"]["68% expected"]),
                    ("95% expected", d["conf_intervals"]["95% expected"])
                 ])

    min_y = 80 if ratio else 10
    max_y = 1500 if ratio else 200
    
    if do_ratio:
        min_y = 0.5
        max_y = 2
        cls = None
    
    min_x = -6
    max_x = 6
    y_log = logy 
    x_label = r"$c_{2V}$"
    y_label = r"95% CL on $\sigma \times B$(HH$\to bb\tau\tau$) [fb]" if not ratio else r"95% CL on $\sigma/\sigma_{SM}$" 
    if do_ratio:
        y_label = r"Ratio w.r.t the first parameter set"

    fname = scan_plot(plots, cls, legends, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y, x_title=x_label, y_title=y_label,
           text=text, x_log=False, y_log=y_log, do_ratio=do_ratio, step=step, pdf_output_path=output_name.format("_logy" if y_log else ""))
    return fname


def main_comparison():
    #dump_francesco(folder="/eos/user/f/fbrivio/Hhh_1718/datacards_VBFtest/cards_TauTauHHbtagclassesV1/comb_cat/", filename="dump_francesco_mpp.json")

    filenames = OrderedDict([
            ("Francesco (raw dnn output)", "dump_francesco.json"),
            ("Jaime (raw dnn output)", "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/prod_v1_ppt_kl0_no50/scan_plot_dnn_hh_vbf_tautau_c2v.json"),
            ("Francesco (mpp)", "dump_francesco_mpp.json"),
            ("Jaime (mpp)", "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/prod_v1_ppt_10bin_new/scan_plot__mpp__tautau__c2v.json"),
            #("Jaime (mpp, no sig)", "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/prod_v1_ppt_10bin_sig/scan_plot__mpp__tautau__c2v.json"),
        #"/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/prod_v1_ppt_10bin_big/scan_plot_dnn_hh_vbf_tautau_c2v.json"
    ])

    legends = [
        #"Francesco", 
        #"Jaime"
        #"With kl=0",
        #"With kl=2.45"
    ]


    plot_scans(filenames.values(), filenames.keys(), output_name) 

def copy_confusion(folder, ids, files, path="/eos/home-j/jleonhol/www/multiclass/hyperscan/"):
    from shutil import copyfile
    seeds = "_".join([str(num) for num in  range(1,11)])
    folders = [folder + s for s in files]
    for id, f in zip(ids, folders):
        if not os.path.isdir(f):
            print f
            continue
        for i in os.listdir(f):
            copyfile(f + i, path + str(id) + "_" + i)

def add_extra():
    # Extra folders
    extra_folders = [
        #"/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_os_even__FT_lbn__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_gce__L2_2p00e-03__EW_1__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/dev1_eventweights_2/",
    #    "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016_2017_2018/CF_default__TC_vbf_common_os_even__FT_lbn__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-02__EW_1__LR_5p00e-04__DO_0p0__BN_1__BS_1024__RS_1/cat_vbf_loose/hyperopt1/",
     #   "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016_2017_2018/CF_default__TC_vbf_common_os_even__FT_lbn_light__AR_lbn_dense_30_extended_128_128_128_128_tanh__LN_wsgce__L2_6p00e-04__EW_1__LR_5p00e-05__DO_0p0__BN_1__BS_1024__RS_1/cat_vbf_loose/hyperopt1/",
    #    "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/prod_v1_ppt_10bin_new/",
    ]
    extra_folders_opt = [
        #"/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_os_even__FT_lbn__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_gce__L2_2p00e-03__EW_1__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/dev1_eventweights_2_opt/",
     #   "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016_2017_2018/CF_default__TC_vbf_common_os_even__FT_lbn__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-02__EW_1__LR_5p00e-04__DO_0p0__BN_1__BS_1024__RS_1/cat_vbf_loose/hyperopt1_opt/",
      #  "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016_2017_2018/CF_default__TC_vbf_common_os_even__FT_lbn_light__AR_lbn_dense_30_extended_128_128_128_128_tanh__LN_wsgce__L2_6p00e-04__EW_1__LR_5p00e-05__DO_0p0__BN_1__BS_1024__RS_1/cat_vbf_loose/hyperopt1_opt/",
     #   "/eos/user/j/jleonhol/hmc/ScanPlot/base_2016/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/cat_vbf_loose/prod_v1_ppt_10bin_opt/",
    ]
    extra_ids = [
        #"gce",
    #    42,
    #   108,
     #   "v1",
    ]

    return extra_folders, extra_folders_opt, extra_ids
    


def main_hyperparam(options):
    from collections import OrderedDict
    template = "CF_{0[0]}__TC_{0[1]}__FT_{0[2]}__AR_{0[3]}__LN_{0[4]}__L2_{0[5]}__EW_1__LR_{0[6]}__DO_{0[7]}__BN_1__BS_1024__RS_{1}/"
    a = []
    # a.append(("default", ["lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "wsgce", "2p00e-03", "5p00e-05", "0p1"]))
    #a.append((39, ["vbf_common_os_even", "lbn"      ,"lbn_dense:30:default:128_128_128_128:tanh", "wsgce", "2p00e-02", "1p00e-05", "0p0"]))
    #a.append((131, ["vbf_common_os_even", "lbn"      ,"lbn_dense:30:extended:128_128_128_128:tanh", "wsgce", "6p00e-03", "1p00e-05", "0p0"]))
    #a.append((203, ["vbf_common_os_even", "lbn_light","lbn_dense:30:extended:256_256_256_256:tanh", "wsgce", "6p00e-04", "1p00e-05", "0p0"]))
    #a.append(280, ["vbf_common_os_even", "lbn_light","lbn_dense:30:extended:256_256_256_256:tanh", "wsgce", "2p00e-02", "5p00e-05", "0p1"]))
    #a.append(240, ["vbf_common_os_even", "lbn_light","lbn_dense:30:extended:256_256_256_256:tanh", "wsgce", "2p00e-03", "5p00e-05", "0p05"]))
    #a.append((12, ["vbf_common_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "wsgce", "6p00e-04", "5p00e-05", "0p0"]))
    #a.append((43, ["vbf_common_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "wsgce", "6p00e-04", "1p00e-05", "0p05"]))
    #a.append(("51_even", ["vbf_common_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "wsgce", "6p00e-03", "1p00e-05", "0p05"]))
    #a.append(("gce", ["vbf_common_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "2p00e-03", "5p00e-05", "0p1"]))
    
    
    ## Normal ones
    a = [
        ("51_gce_even", ["default", "vbf_common_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        #("51_gce_odd", ["default", "vbf_common_os_odd", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        ("51_gce_ce", ["default", "vbf_common_os", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        ("51_gce_loose_even", ["default", "vbf_loose_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        #("51_gce_loose_odd", ["default", "vbf_loose_os_odd", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        ("51_gce_loose_ce", ["default", "vbf_loose_os", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]), 
        ("51_gce_nlo_even", ["default_nlo", "vbf_common_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        #("51_gce_nlo_odd", ["default_nlo", "vbf_common_os_odd", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        ("51_gce_nlo_ce", ["default_nlo", "vbf_common_os", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        ("51_gce_nlo_loose_even", ["default_nlo", "vbf_loose_os_even", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        #("51_gce_nlo_loose_odd", ["default_nlo", "vbf_loose_os_odd", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
        ("51_gce_nlo_loose_ce", ["default_nlo", "vbf_loose_os", "lbn_light","lbn_dense:30:default:128_128_128_128:tanh", "gce", "6p00e-03", "1p00e-05", "0p05"]),
    ]

    grouped_ids = {
        "even": ["51_gce_even", "51_gce_loose_even", "51_gce_nlo_even", "51_gce_nlo_loose_even"],
        "odd": ["51_gce_odd", "51_gce_loose_odd", "51_gce_nlo_odd", "51_gce_nlo_loose_odd"],
        "ce": ["51_gce_ce", "51_gce_loose_ce", "51_gce_nlo_ce", "51_gce_nlo_loose_ce"],
    }



    if options.year == 2016:
        folder = "/eos/home-j/jleonhol/hmc/ScanPlot/base_2016_2017_2018/"
    elif options.year == 2017:
        folder = "/eos/home-j/jleonhol/hmc/ScanPlot/base_2017_2016_2018/"
    elif options.year == 2018:
        folder = "/eos/home-j/jleonhol/hmc/ScanPlot/base_2018_2016_2017/"
    else:
        raise ValueError("2016, 2017 and 2018 are the only posible years")
    seeds = "_".join([str(num) for num in  range(1,11)])
  

    stuff = OrderedDict(a)
    ids = stuff.keys()

    confusion_folders =  [template.format(s, seeds).replace(":","_") + "cat_vbf_loose/hyperopt1/" for s in stuff.values()]
    # copy_confusion("/eos/home-j/jleonhol/hmc/ConfusionPlot/base_2016_2017_2018/", ids, confusion_folders)

    folders = [folder + template.format(s, seeds).replace(":","_") + "cat_vbf_loose/" for s in stuff.values()]
    postfix = "" if not options.ratio else "__ratio"
    files = {"raw": "scan_plot__tautau__c2v{}.json".format(postfix), "mpp": "scan_plot__mpp__tautau__c2v{}.json".format(postfix)}
   
    for f in files.values():
        assert options.channel in f

    stuff = OrderedDict(zip(ids, folders))

    extra_folders, extra_folders_opt, extra_ids = add_extra()


    channel = r"${}$ channel".format(options.channel)
    channel = channel.replace("tau", "\\tau").replace("mu", "\\mu")
    year = r"{}".format(options.year)
    text = [year, channel]

    
    version = ["hyperopt1/"]
    version_opt = ["hyperopt1_opt/"]
    if options.year == 2016 and False:
        version += ["hyperopt1_nlo/"]
        version_opt += ["hyperopt1_nlo_opt/"]

    for f,id in zip(folders, ids):
        for cat in files:
            fil = files[cat]
            for v in version:
                if not os.path.isfile(f + v + fil):
                    print "({}, {}, {})".format(v, id, cat), "not found"
                    #print f + v + fil,"({}, {}, {})".format(v, id, cat), "not found"
            for v in version_opt:
                if not os.path.isfile(f + "hyperopt1_opt/" + fil):
                    print "({}, {}, {})".format(v, id, cat), "not found"
                    #print f + v + fil,"({}, {}, {})".format(v, id, cat), "not found"
    
    for f in extra_folders + extra_folders_opt:
        for fil in files.values():
            if not os.path.isfile(f + fil):
                print f + fil, "not found"



    print "first"

    files_to_copy = []

    # All raw, all mpp
    for key in files:
        legends = []
        filenames = []
        for id, f in zip(ids, folders):
            for v in version:
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legends.append(legend)
                filenames.append(f + v + files[key])
        for id, f in zip(extra_ids, extra_folders):
            legends.append("{}_{}".format(id, key))
            filenames.append(f + files[key])
        if filenames:
            postfix = key
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=options.ratio, text=text))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text))
    
    # grouped raw or mpp
    for key in files:
        for group_name in grouped_ids:
            legends = []
            filenames = []
            for id in grouped_ids[group_name]:
                if id not in stuff:
                    continue
                f = stuff[id]
                for v in version:
                    if not os.path.isfile(f + v + files[key]):
                        continue
                    legend = "{}_{}".format(id, key)
                    if "nlo" in v:
                        legend += "_nlo"
                    legends.append(legend)
                    filenames.append(f + v + files[key])
                if filenames:
                    postfix = "{}_{}".format(group_name, key)
                if options.ratio:
                    postfix += "_mu"
                files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=1))
                files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=1))
                if options.ratio:
                    continue
                postfix += "_ratio"
                files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=1))
    
    # Individual, raw vs mpp
    for id, f in zip(ids, folders):
        legends = []
        filenames = []
        for key in files:
            for v in version:
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legends.append(legend)
                filenames.append(f + v + files[key])
        if filenames:
            postfix = str(id)
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=1))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=1))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=1))
    
    for id, f in zip(extra_ids, extra_folders):
        legends = []
        filenames = []
        for key in files:
            legends.append("{}_{}".format(id, key))
            filenames.append(f + files[key])
        if filenames:
            postfix = str(id)
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=1))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=1))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=1))

    ############ Opt
    for key in files:
        legends = []
        filenames = []
        for id, f in zip(ids, folders):
            for v in version:
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legends.append(legend)
                filenames.append(f + v + files[key])
            for v in version_opt:
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legend += "_opt" 
                legends.append(legend)
                filenames.append(f + v + files[key])
        for i, id in enumerate(extra_ids):
            if i >= len(extra_folders):
                continue
            if not os.path.isfile(extra_folders[i] + files[key]):
                continue
            if i >= len(extra_folders_opt):
                continue
            if not os.path.isfile(extra_folders_opt[i] + files[key]):
                continue
            legends.append("{}_{}".format(id, key))
            filenames.append(extra_folders[i] + files[key])
            legends.append("{}_{}_opt".format(id, key))
            filenames.append(extra_folders_opt[i] + files[key])

        if filenames:
            postfix = key
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=2))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=2))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=2))
    
    #opt only
    for key in files:
        legends = []
        filenames = []
        for v in version_opt:
            for id, f in zip(ids, folders):
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legend += "_opt" 
                legends.append(legend)
                filenames.append(f + v + files[key])
        for i, id in enumerate(extra_ids):
            if i >= len(extra_folders_opt):
                continue
            if not os.path.isfile(extra_folders_opt[i] + files[key]):
                continue
            legends.append("{}_{}_opt".format(id, key))
            filenames.append(extra_folders_opt[i] + files[key])

        if filenames:
            postfix = key
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=2))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=2))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=2))
    
    
    # grouped raw or mpp
    for key in files:
        for group_name in grouped_ids:
            legends = []
            filenames = []
            for id in grouped_ids[group_name]:
                if id not in stuff:
                    continue
                f = stuff[id]
                for v in version_opt:
                    if not os.path.isfile(f + v + files[key]):
                        continue
                    legend = "{}_{} (opt)".format(id, key)
                    if "nlo" in v:
                        legend += "_nlo"
                    legends.append(legend)
                    filenames.append(f + v + files[key])
                if filenames:
                    postfix = "{}_{}".format(group_name, key)
                if options.ratio:
                    postfix += "_mu"
                files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=1))
                files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=1))
                if options.ratio:
                    continue
                postfix += "_ratio"
                files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=1))
    
    
    for id, f in zip(ids, folders):
        legends = []
        filenames = []
        for key in files:
            for v in version:
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legends.append(legend)
                filenames.append(f + v + files[key])
            for v in version_opt:
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legend += "_opt" 
                legends.append(legend)
                filenames.append(f + v + files[key])
        if filenames:
            postfix = str(id)
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=1))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=1))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=1))
    
    #opt only
    for id, f in zip(ids, folders):
        legends = []
        filenames = []
        for key in files:
            for v in version_opt:
                if not os.path.isfile(f + v + files[key]):
                    continue
                legend = "{}_{}".format(id, key)
                if "nlo" in v:
                    legend += "_nlo"
                legend += "_opt" 
                legends.append(legend)
                filenames.append(f + v + files[key])
        if filenames:
            postfix = str(id)
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=1))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=1))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=1))

    for i, id in enumerate(extra_ids):
        legends = []
        filenames = []
        for key in files:
            if i >= len(extra_folders):
                continue
            if not os.path.isfile(extra_folders[i] + files[key]):
                continue
            if i >= len(extra_folders_opt):
                continue
            if not os.path.isfile(extra_folders_opt[i] + files[key]):
                continue
            legends.append("{}_{}".format(id, key))
            filenames.append(extra_folders[i] + files[key])
            legends.append("{}_{}_opt".format(id, key))
            filenames.append(extra_folders_opt[i] + files[key])
        if filenames:
            postfix = str(id)
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=2))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=2))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_opt".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=2))
    #opt only
    for i, id in enumerate(extra_ids):
        legends = []
        filenames = []
        for key in files:
            if i >= len(extra_folders_opt):
                continue
            if not os.path.isfile(extra_folders_opt[i] + files[key]):
                continue
            legends.append("{}_{}_opt".format(id, key))
            filenames.append(extra_folders_opt[i] + files[key])
        if filenames:
            postfix = str(id)
            if options.ratio:
                postfix += "_mu"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=options.ratio, text=text, step=1))
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", True, ratio=options.ratio, text=text, step=1))
            if options.ratio:
                continue
            postfix += "_ratio"
            files_to_copy.append(plot_scans(filenames, legends, "hyperscan/comparison_{}_optonly".format(postfix) + "{}.pdf", ratio=False, do_ratio=True, text=text, step=1))

    if options.copy:
        output_folder = "hyperscan_{}/".format(options.year)
        copy_index("", "/eos/home-j/jleonhol/www/multiclass/" + output_folder, files_to_copy, options.delete)





if __name__ == '__main__' :
    options = parse_args()
    main_hyperparam(options)
    

    
   
    
    
