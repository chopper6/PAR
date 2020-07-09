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

params = ({'model_file':'base_model_v2.ka','experiment':'hist', 'repeats':2, 
	'time':1000, 'timestamp':util.timestamp(),
	'species':{'NAD':10000, 'PARG':0, 'PARP':20},
	'variables': {'init_DNA':20,'elong_boost':400, 'endo_inhib': 1.0E-2, 
	'PARP_2_PARG': 3,'base_fwd':1.0E+2, 'base_rev':1.0E-2, 'base_catalysis':1.0E+5},
	'out_dir':'./output/', 'write_params_on_img':1, 'save_fig':0, 'dpi':300, 'std_devs':1})

# prev
#params = ({'experiment':'sweep', 'repeats':20, 'time':100000, 'timestamp':util.timestamp(), 
#	'NAD':10000, 'PARG':0, 'DNA': 20, 'PARP':20,
#	'base_fwd':1.0E+4, 'base_rev':1.0E-2, 'catalysis_rate':1.0E+8, 'cut_rate':1.0E-8,
#	'out_dir':'./output/local/', 'write_params_on_img':False, 'save_fig':True, 'dpi':300, 'std_devs':1})
