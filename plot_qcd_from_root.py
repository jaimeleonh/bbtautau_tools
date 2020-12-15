import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)

import os
from copy import deepcopy as copy
from math import sqrt
from collections import OrderedDict

# filename = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau/root/DNNoutSM_kl_1__pg_plots__tautau_os_inviso.root"
filenames = OrderedDict()
filenames["os_iso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau/root/DNNoutSM_kl_1__pg_plots__qcd__tautau_os_iso.root"
filenames["ss_iso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau/root/DNNoutSM_kl_1__pg_plots__tautau_ss_iso.root"
filenames["os_inviso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau/root/DNNoutSM_kl_1__pg_plots__tautau_os_inviso.root"
filenames["ss_inviso"] = "/eos/user/j/jleonhol/hmc/FeaturePlot/base_2016/cat_resolved_2b/qcd_test__tautau/root/DNNoutSM_kl_1__pg_plots__tautau_ss_inviso.root"

other_regions = ["ss_iso", "os_inviso", "ss_inviso"]
processes = ["tth", "full_others", "dy", "tt", "data"]

def get_histos(filename):
    tfile = r.TFile.Open(filename)
    bkg_histo = None
    data_histo = None
    bkg_histos = {}
    table = []
    tdir = tfile.Get("histograms")
    for tkey in tdir.GetListOfKeys():
        thist = tdir.Get(tkey.GetName())
        if not isinstance(tdir.Get(tkey.GetName()), r.TH1F):
            continue
        for process in processes:
            if (process + "_") in thist.GetName():
                if not "data" in process:
                    row = [process]
                    if not bkg_histo:
                        bkg_histo = thist.Clone("bkg")
                    else:
                        bkg_histo.Add(thist)
                    for ibin in range(1, thist.GetNbinsX() + 1):
                        value = thist.GetBinContent(ibin)
                        error = thist.GetBinError(ibin)
                        dec = 1
                        while (True):
                            if round(value, dec + 1) != 0 and round(error, dec + 1) != 0:
                                value = round(value, dec + 1)
                                error = round(error, dec + 1)
                                break
                            if dec == 10:
                                break
                            dec += 1
                        row.append("{} +- {}".format(value, error))
                    table.append(row)
                elif "data" in thist.GetName():
                    data_histo = thist.Clone()
                bkg_histos[process] = thist.Clone()
    return copy(bkg_histo), copy(data_histo), copy(bkg_histos)


def get_row(process_name, histo, scaling = 1., blind_range = (999, 999)):
    row = [process_name]
    for ibin in range(1, histo.GetNbinsX() + 1):
        value = histo.GetBinContent(ibin)
        error = histo.GetBinError(ibin)
        dec = 1
        while (True):
            if round(value, dec + 1) != 0 and round(error, dec + 1) != 0:
                value = round(value, dec + 1)
                error = round(error, dec + 1)
                break
            if dec == 10:
                break
            dec += 1
        if histo.GetBinCenter(ibin) > blind_range[0] and histo.GetBinCenter(ibin) < blind_range[1]:
            row.append("-")
        else:
            row.append("{} +- {}".format(value, error))
    return row

bkg_histo = {}
data_histo = {}
bkg_histos = {}

bkg_histo["os_iso"], data_histo["os_iso"], bkg_histos["os_iso"] = get_histos(filenames["os_iso"])
bkg_histo["ss_iso"], data_histo["ss_iso"], bkg_histos["ss_iso"] = get_histos(filenames["ss_iso"])
bkg_histo["os_inviso"], data_histo["os_inviso"], bkg_histos["os_inviso"] = get_histos(filenames["os_inviso"])
bkg_histo["ss_inviso"], data_histo["ss_inviso"], bkg_histos["ss_inviso"] = get_histos(filenames["ss_inviso"])

data_histo["ss_iso"].Add(bkg_histo["ss_iso"], -1)
data_histo["os_inviso"].Add(bkg_histo["os_inviso"], -1)
data_histo["ss_inviso"].Add(bkg_histo["ss_inviso"], -1)

def get_integral_and_error(hist):
    error = r.Double()
    integral = hist.IntegralAndError(0, hist.GetNbinsX() + 1, error)
    error = float(error)
    compatible = True if integral - error <= 0 else False
    return integral, error, compatible

ss_iso_integral, ss_iso_integral_error, _ = get_integral_and_error(data_histo["ss_iso"])
ss_inviso_integral, ss_inviso_integral_error, _ = get_integral_and_error(data_histo["ss_inviso"])

print ss_iso_integral, ss_iso_integral_error
print ss_inviso_integral, ss_inviso_integral_error,

qcd_histo = data_histo["os_inviso"].Clone()

new_errors = [(qcd_histo.GetBinError(i)/qcd_histo.GetBinContent(i))**2 for i in range(1, qcd_histo.GetNbinsX() + 1)]
new_errors = [elem + (ss_iso_integral_error/ss_iso_integral)**2 + (ss_inviso_integral_error/ss_inviso_integral)**2 for elem in new_errors]

qcd_histo.Scale(ss_iso_integral / ss_inviso_integral)
for ibin in range(1, qcd_histo.GetNbinsX() + 1):
    qcd_histo.SetBinError(ibin, sqrt(new_errors[ibin - 1]) * qcd_histo.GetBinContent(ibin))

tables = OrderedDict()
for region in filenames:
    tables[region] = []

for region in other_regions:
    for process in processes[:-1]:
        tables[region].append(get_row(process, bkg_histos[region][process]))
    tables[region].append(get_row("qcd", data_histo[region]))

c = r.TCanvas("name", "name", 800, 800)
data_histo["os_inviso"].Draw()
c.SetLogy()
c.SaveAs("qcd_log.pdf")
del c 

tables["os_iso"] = []
for process in processes[:-1]:
    tables["os_iso"].append(get_row(process, bkg_histos["os_iso"][process]))
tables["os_iso"].append(get_row("bkg_sum", bkg_histo["os_iso"]))
tables["os_iso"].append(get_row("qcd", qcd_histo))
tables["os_iso"].append(get_row("data", data_histo["os_iso"], blind_range=(0.5, 1)))

def print_table(region, table, latex=False):
    import tabulate
    headers = ["process / bin"] + [i for i in range(1, bkg_histo["os_iso"].GetNbinsX() + 1)]
    print "*" * 20
    print "{:^20}".format(region)
    print "*" * 20

    if latex:
        new_table = copy(table)
        for line in new_table:
            for i, elem in enumerate(line):
                if "_" in elem:
                    line[i] = line[i].replace("_", "\\_")
                if "+-" in elem:
                    line[i] = line[i].replace("+-", "\\pm")
                    line[i] = "$ " + line[i] + " $"
        print tabulate.tabulate(new_table, headers=headers, tablefmt="latex_raw")
    else:
        print tabulate.tabulate(table, headers=headers)
        
for region in tables:
    print_table(region, tables[region], latex=False)
