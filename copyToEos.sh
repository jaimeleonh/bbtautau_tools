# for year in 2016 2017 2018
# do
	# mkdir "$multiclassWWW"/qcd_unc/"$year"/
	# cp "$multiclassWWW"/qcd_unc/index.php "$multiclassWWW"/qcd_unc/"$year"/
	# for cat in boosted resolved_1b resolved_2b
	# do
		# mkdir "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
		# cp "$multiclassWWW"/qcd_unc/index.php "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
		# for chan in mutau etau tautau
		# do
			# for region in os_inviso ss_inviso
			# do
				# for wp in vvvl_vvl vvl_vl vl_l l_m
				# do
					# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"__"$wp"/lep1_pt__"$chan"_"$region"__"$wp"__stack__qcd_wp_"$wp".pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
				# done
				# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"__NO_STR/lep1_pt__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
				# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"/lep1_eta__pg_plots__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
			# done
			# for region in ss_iso
			# do
				# for wp in vvvl_vvl vvl_vl vl_l l_m
				# do
					# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"__"$wp"/lep1_pt__"$chan"_"$region"__stack__qcd_wp_"$wp".pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
				# done
				# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"__NO_STR/lep1_pt__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
				# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"/lep1_eta__pg_plots__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
			# done
			# for region in os_iso
			# do
				# for wp in vvvl_vvl vvl_vl vl_l l_m
				# do
					# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"__"$wp"/lep1_pt__qcd__"$chan"_"$region"__stack__qcd_wp_"$wp".pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
				# done
				# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"__NO_STR/lep1_pt__qcd__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
				# cp /eos/user/j/jleonhol/hmc/FeaturePlot/base_"$year"//cat_$cat/qcd_test__new__"$chan"/lep1_eta__pg_plots__qcd__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
			# done

		# done
		# cd "$multiclassWWW"/qcd_unc/"$year"/"$cat"/
		# find . -type f -name "*.pdf" -exec pdftocairo -singlefile -cropbox -png {} \;
		# cd -
	# done
# done

training=CF_default__TC_vbf_os__FT_lbn_light__AR_lbn_dense_30_default_0_4_tanh__LN_bsm__L2_1p00e+00__EW_0__LR_1p00e+00__DO_1p0__BN_1__BS_1024__RS_1_2_3_4_5_6_7_8_9_10

# VBF multicategories
for year in 2016_2017_2018 2017_2016_2018 2018_2016_2017
do
		for cat in vbf
		do
				mkdir "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
				cp "$multiclassWWW"/qcd_unc/index.php "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
				for chan in mutau etau tautau
				do
						for feature in hh_vbf_sm_c2v hh_ggf tt dy tth
						do
								for region in os_inviso ss_inviso
								do
										for wp in vvvl_vvl vvl_vl vl_l l_m
										do
												cp /eos/user/j/jleonhol/hmc/TrainingOutputPlot/base_"$year"/"$training"/cat_$cat/qcd_test__new__"$chan"__"$wp"/DNNoutSM_kl_1_"$feature"_merged_mpp__"$chan"_"$region"__"$wp"__stack__qcd_wp_"$wp".pdf "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
										done
										cp /eos/user/j/jleonhol/hmc/TrainingOutputPlot/base_"$year"/"$training"/cat_$cat/qcd_test__new__"$chan"__NO_STR/DNNoutSM_kl_1_"$feature"_merged_mpp__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
								done
								for region in ss_iso
								do
										for wp in vvvl_vvl vvl_vl vl_l l_m
										do
												cp /eos/user/j/jleonhol/hmc/TrainingOutputPlot/base_"$year"/"$training"/cat_$cat/qcd_test__new__"$chan"__"$wp"/DNNoutSM_kl_1_"$feature"_merged_mpp__"$chan"_"$region"__stack__qcd_wp_"$wp".pdf "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
										done
										cp /eos/user/j/jleonhol/hmc/TrainingOutputPlot/base_"$year"/"$training"/cat_$cat/qcd_test__new__"$chan"__NO_STR/DNNoutSM_kl_1_"$feature"_merged_mpp__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
								done
								for region in os_iso
								do
										for wp in vvvl_vvl vvl_vl vl_l l_m
										do
												cp /eos/user/j/jleonhol/hmc/TrainingOutputPlot/base_"$year"/"$training"/cat_$cat/qcd_test__new__"$chan"__"$wp"/DNNoutSM_kl_1_"$feature"_merged_mpp__qcd__blinded__"$chan"_"$region"__stack__qcd_wp_"$wp".pdf "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
										done
										cp /eos/user/j/jleonhol/hmc/TrainingOutputPlot/base_"$year"/"$training"/cat_$cat/qcd_test__new__"$chan"__NO_STR/DNNoutSM_kl_1_"$feature"_merged_mpp__qcd__blinded__"$chan"_"$region"__stack.pdf "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
								done
						done
				done
				cd "$multiclassWWW"/qcd_unc/${year:0:4}/"$cat"/
				find . -type f -name "*.pdf" -exec pdftocairo -singlefile -cropbox -png {} \;
				cd -
		done
	
	
done
