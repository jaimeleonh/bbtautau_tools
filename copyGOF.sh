mkdir "$multiclassWWW"/GOFtests
cp "$multiclassWWW"/index.php "$multiclassWWW"/GOFtests
for year in 2016
do
  mkdir "$multiclassWWW"/GOFtests/"$year"
  cp "$multiclassWWW"/index.php "$multiclassWWW"/GOFtests/"$year"/
  for channel in tautau
  do
    mkdir "$multiclassWWW"/GOFtests/"$year"/"$channel"
    cp "$multiclassWWW"/index.php "$multiclassWWW"/GOFtests/"$year"/"$channel"/
    
    mkdir "$multiclassWWW"/GOFtests/"$year"/"$channel"/distributions/
    cp "$multiclassWWW"/index.php "$multiclassWWW"/GOFtests/"$year"/"$channel"/distributions/
    cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"/cat_vbf/test_new_"$channel"/*"$channel"_os_iso*.pdf "$multiclassWWW"/GOFtests/"$year"/"$channel"/distributions/
    cd "$multiclassWWW"/GOFtests/"$year"/"$channel"/distributions/
    find . -type f -name "*.pdf" -exec pdftocairo -singlefile -cropbox -png {} \;
    cd -
    
    mkdir "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF/
    cp "$multiclassWWW"/index.php "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF/
    cp /eos/user/j/jleonhol/hmc/RunGoodnessOfFit/base_"$year"/test_new_"$channel"/*.pdf "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF/
    cd "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF/
    find . -type f -name "*.pdf" -exec pdftocairo -singlefile -cropbox -png {} \;
    cd -
    
    mkdir "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF_Summary/
    cp "$multiclassWWW"/index.php "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF_Summary/
    cp /eos/user/j/jleonhol/hmc/SummarizeGoodnessOfFit/base_"$year"/test_new_"$channel"/*.pdf "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF_Summary/
    cd "$multiclassWWW"/GOFtests/"$year"/"$channel"/GOF_Summary/
    find . -type f -name "*.pdf" -exec pdftocairo -singlefile -cropbox -png {} \;
    cd -
    

  done
done
