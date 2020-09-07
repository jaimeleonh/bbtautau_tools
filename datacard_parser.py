import os
from collections import OrderedDict
import ROOT
ROOT.gROOT.SetBatch(True)
from copy import deepcopy

filename = "/eos/user/j/jleonhol/hmc/CreateDatacards/base_2016/cat_vbf_loose/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/prod_v1_newntup/datacards/cards_tautau/vbf_loosednn_hh_vbf/hh_2_C4_13TeV.txt"


filenames =[ 
    "/eos/user/j/jleonhol/hmc/CreateDatacards/base_2016/cat_vbf_loose/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/prod_v1_ppt_10bin_new/datacards_mpp/cards_tautau/vbf_loosednn_hh_vbf_merged_mpp/hh_2_C4_dnn_hh_vbf_merged_mpp_13TeV.txt"
    #"/eos/user/j/jleonhol/hmc/CreateDatacards/base_2016/cat_vbf_loose/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/prod_v1_ppt_kl0_no50/datacards/cards_tautau/vbf_loosednn_hh_vbf/hh_2_C4_13TeV.txt"
    ,
    "/eos/user/f/fbrivio/Hhh_1718/datacards_VBFtest/cards_TauTauHHbtagclassesV1/VBFclassmdnn__v1__kl1_c2v1_c31__hh_vbf/hh_2_C12_13TeV.txt"
    #"/eos/user/f/fbrivio/Hhh_1718/datacards_VBFtest/cards_TauTauHHbtagVBFnodeVBFloose/VBFloosemdnn__v1__kl1_c2v1_c31__hh_vbf/hh_2_C4_13TeV.txt"
]

plotfilenames = [
    #"/eos/user/j/jleonhol/hmc/CreateDatacards/base_2016/cat_vbf_loose/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/prod_v1_ppt_kl0_no50/datacards/cards_tautau/vbf_loosednn_hh_vbf/hh_2_C4_13TeV.input.root"
    "/eos/user/j/jleonhol/hmc/CreateDatacards/base_2016/cat_vbf_loose/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__EW_0__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/prod_v1_ppt_10bin_new/datacards_mpp/cards_tautau/vbf_loosednn_hh_vbf_merged_mpp/hh_2_C4_dnn_hh_vbf_merged_mpp_13TeV.input.root"
    ,
    #"/eos/user/f/fbrivio/Hhh_1718/datacards_VBFtest/cards_TauTauHHbtagVBFnodeVBFloose/VBFloosemdnn__v1__kl1_c2v1_c31__hh_vbf/hh_2_C4_13TeV.input.root"
    "/eos/user/f/fbrivio/Hhh_1718/datacards_VBFtest/cards_TauTauHHbtagclassesV1/VBFclassmdnn__v1__kl1_c2v1_c31__hh_vbf/hh_2_C12_13TeV.input.root"
]

stuff = {}
plots = {}
scaling = {}

for filename, plotfile in zip(filenames, plotfilenames):
    with open(os.path.expandvars(filename)) as f:
        plotf = ROOT.TFile.Open(plotfile)
        lines = f.readlines()
        for i,line in enumerate(lines):
            if line.startswith("process"):
                processes = [process for process in line[:-1].split(" ") if process != ""]
                rates = [rate for rate in lines[i+2][:-1].split(" ") if rate != ""]
                for process,rate in zip(processes, rates):
                    if process == "process" or "ggHH" in process : continue
                    new_process = process
                    new_process = process.lower() if process == "TT" or process == "ttH" or process == "DY" else process
                    if new_process not in stuff:
                        stuff[new_process] = []
                    stuff[new_process].append(rate)

                    if new_process not in plots:
                        plots[new_process] = []
                        scaling[new_process] = []
                    plot = plotf.Get(process)
                    plots[new_process].append(deepcopy(plotf.Get(process)))
                break

pr_rt = []
for process in stuff:
    p = stuff[process]
    print process
    if len(p) == 2:
        if float(p[0]) == 0.:
            stuff[process].append(0.)
        elif float(p[1])/float(p[0]) > 2.:
            stuff[process].append(100*(float(p[1]) - float(p[0])/(0.073)) / float(p[1]))
            scaling[process].append(1./(0.073))
            scaling[process].append(1)
        else:
            stuff[process].append(100*(float(p[1]) - float(p[0])) / float(p[1]))
        pr_rt.append((process, p[0], p[1], p[2]))
    else:
        pr_rt.append((process, p[0], p[1]))
pr_rt_s = sorted(pr_rt, key=lambda x:x[0])
for elem in pr_rt_s:
    str = "{:<35} ".format(elem[0].replace("_","\_"))
    for p in elem[1:]:
        str += "& {:<8.3f} ".format(float(p))
    str += "\\\\"
    print str

folder_name = "plots_datacard_comparison/"
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

def plot_ratio(name, plotlist, scaling, folder):
    c = ROOT.TCanvas("c", "c", 800, 800)
    print name, plotlist[0].Integral(), plotlist[1].Integral()
    plotlist[0].SetLineColor(ROOT.kRed)
    plotlist[1].SetLineColor(ROOT.kBlue)

    miny = 0.
    maxy = 0.
    for i in range(2):
        if plotlist[i].GetMaximum() > maxy:
            maxy = plotlist[i].GetMaximum()
    plotlist[0].SetMinimum(miny)
    plotlist[0].SetMaximum(1.3*maxy)


    leg = ROOT.TLegend(0.8, 0.8, 0.95, 0.95)
    leg.AddEntry(plotlist[0], "Jaime", "l")
    leg.AddEntry(plotlist[1], "Francesco", "l")

    if scaling:
        plotlist[0].Scale(scaling[0])
        plotlist[1].Scale(scaling[1])
    print name, plotlist[0].Integral(), plotlist[1].Integral()
    plotlist[0].Draw()
    plotlist[1].Draw("same")
    leg.Draw("same")
    c.SaveAs(folder + name + ".pdf")
    c.SaveAs(folder + name + ".png")
                


for process in plots:
    if len(plots[process]) == 2:
        plot_ratio(process, plots[process], scaling[process], folder_name)


















