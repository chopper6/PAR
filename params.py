import util 

# Due to 1) huge numbers, 2) unknown numbers, maybe try and capture
# shape of curve without using the real values of proteins..?
# too unconstrained?
# qualitatively match: Turnover1 fig1,2,3,8, if need more few in Turnover3
#						Hatakeyama fig6
#						Braun!!!
# ...to demonstrate change in distrib (1 leading tree + shift to histones)
#		+ biphasic degredation due to tree struct?
# poss add histones as targets of polymerization, rate is lower but #histones > #PARP

# Fig1: 600uL
# [NAD] = 7.2E+16, since [NAD] ~= 1.2E+20 per L
# PARP: sA= 390 units/mgmin, i.e. 1 nmol of ADP-ribose added per min
#	so 1 mg add 2.34E+17 residues per min
#	Fig1 uses 2.7 U (i assume 'units'), so 6.318E+17 residues per min
#	but avg'g is not reliable  

params = ({'model_file':'menard_fig1.ka','output_model_file':'model.ka','experiment':'time', 'repeats':2, 
	'time':3, 'timestamp':util.timestamp(), 'num_snapshots':60,
	'species':{'NAD':1000, 'PARG':0, 'PARP':100}, 
	'variables': {'init_DNA':10,'elong_boost':400, 'endo_inhib': 0, 'amt_PARG_to_add': 10,
	'PARP_2_PARG': 1,'base_fwd':5.0E-1, 'base_rev':1.0E-6, 'base_catalysis':1.0E+6},
	'out_dir':'./output/', 'write_params_on_img':1, 'save_fig':0, 'dpi':100,
	'use_CI':0,'std_devs':3})

# prev
#params = ({'experiment':'sweep', 'repeats':20, 'time':100000, 'timestamp':util.timestamp(), 
#	'NAD':10000, 'PARG':0, 'DNA': 20, 'PARP':20,
#	'base_fwd':1.0E+4, 'base_rev':1.0E-2, 'catalysis_rate':1.0E+8, 'cut_rate':1.0E-8,
#	'out_dir':'./output/local/', 'write_params_on_img':False, 'save_fig':True, 'dpi':300, 'std_devs':1})
