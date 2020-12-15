import os, shutil

def copy_index(input_f, output_f, list_of_files=[], delete=True):
    is_php = False
    if not os.path.isdir(output_f):
        os.mkdir(output_f)
    if delete:
        for f in os.listdir(output_f):
            if f.endswith(".png") or f.endswith(".pdf"):
                os.remove(output_f + f)
            if ".php" in f:
                is_php = True
    if not is_php:
        end_char = 2 if output_f.endswith("/") else 1
        back_folder = "/".join(output_f.split("/")[0:-end_char])
        shutil.copyfile(back_folder + "/index.php", output_f + "/index.php")

    if not list_of_files:
        list_of_files = os.listdir(input_f)
        print list_of_files
    for f in list_of_files:
        print input_f + f
        output_file = f.split("/")[-1]
        if not os.path.isdir(input_f + f):
            shutil.copyfile(input_f + f, output_f + output_file)    
    shutil.copyfile(input_f + f, output_f + output_file)
    cmd1 = 'find . -maxdepth 1 -type f -name "*.pdf" -exec pdftocairo -singlefile -cropbox -png {} \;'
    os.chdir(output_f)
    os.popen(cmd1)

if __name__ == "__main__":
    copy_index("/eos/user/j/jleonhol/hmc/FeaturePlot/base_2018/cat_vbf_loose/dmc/", "/eos/home-j/jleonhol/www/multiclass/data_mc_plots/vbf_loose/")
    #copy_index("./hyperscan/", "/eos/home-j/jleonhol/www/multiclass/hyperscan_2016/")
