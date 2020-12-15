import ROOT as r
r.gROOT.SetBatch(True)


francesco = r.TFile("/eos/user/j/jleonhol/HHbbtautau/SKIMS_1June2020/SKIM_VBFHH_CV_1_C2V_1_C3_1/output_0.root")
#francesco = r.TFile("/eos/user/f/fbrivio/Hhh_1718/datacards_VBFtest/1Sept2020/SKIM_VBFHHTo2B2Tau_CV_1_C2V_1_C3_1/output_0.root")
jaime = r.TFile("/eos/user/j/jleonhol/hmc/EvaluateData/base_2018/CF_default__TC_vbf_common_odd__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_wsgce__L2_2p00e-03__LR_5p00e-05__DO_0p1__BN_1__BS_1024__RS_1/hh_vbf/cat_vbf_loose_even/prod_v1/data_0.root")
#jaime = r.TFile("/eos/user/j/jleonhol/hmc/EvaluateData/base_2018_2016_2017/CF_default__TC_vbf_common_os_even__FT_lbn_light__AR_lbn_dense_30_default_128_128_128_128_tanh__LN_gce__L2_6p00e-03__EW_1__LR_1p00e-05__DO_0p05__BN_1__BS_1024__RS_1_2_3_4_5_6_7_8_9_10/hh_vbf/cat_vbf_loose_even/hyperopt1/data_0.root")
tree = francesco.Get("HTauTauTree")
nentries = tree.GetEntries()
#for i in  tree.GetListOfBranches():
#    print i.GetName()

treej = jaime.Get("evaluation")
nentriesj = tree.GetEntries()

for i in  treej.GetListOfBranches():
    print i.GetName()

node_list = ["hh_vbf", "hh_ggf", "dy", "tth", "tt_lep", "tt_fh"]
node_list_j = ["hh_vbf", "hh_ggf", "dy", "tth_tautau", "tth_bb", "tt_sl", "tt_dl", "tt_fh"]



for j in range(nentriesj):
    treej.GetEntry(j)
#    print treej.GetBranch("EventNumber").GetLeaf("EventNumber").GetValue()



for i in range(nentries):
    tree.GetEntry(i)
    eventNum = int(tree.GetBranch("EventNumber").GetLeaf("EventNumber").GetValue())
    
    #if eventNum != 298802: continue
    
    #for node in node_list:
    #    name = "mdnn__v2__kl1_c2v1_c31__" + node
    #    print "{}:{:.3f}".format(node, tree.GetBranch(name).GetLeaf(name).GetValue()),
    #print ""

    for j in range(nentriesj):
        treej.GetEntry(j)
        if int(treej.GetBranch("EventNumber").GetLeaf("EventNumber").GetValue()) == eventNum:
            print "F", eventNum,
            for node in node_list:
                name = "mdnn__v1__kl1_c2v1_c31__" + node
                print "{}:{:.3f}".format(node, tree.GetBranch(name).GetLeaf(name).GetValue()),
            print ""
            print "J", eventNum,
            for node in node_list_j:
                name = "dnn_" + node
                print "{}:{:.3f}".format(node, treej.GetBranch(name).GetLeaf(name).GetValue()),
            print ""
            break
    

