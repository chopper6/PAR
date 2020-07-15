import util, plot, features
from util import rng
import kappy
from copy import deepcopy

from params import params

def main():
	if params['experiment'] == 'hist':
		hist()
	elif params['experiment'] == 'sweep':
		sweep()
	elif params['experiment'] in ['time','time_series']:
		time_series()
	else: 
		assert(False) #unknown 'experiment' param

	print("\n\n Done. \n\n")


############################################### EXPERIMENTS ###############################################
'''
def fig1_part1():
	# tuning params: 'elong_boost', 'NAD', 'PARP', 'base_fwd', 'base_rev', 'base_catalysis'
	params['PARP_2_PARG'] = 3
	params['time'] = 1
	params['PARG'] = 0


def fig1_part2():
	# tuning params: 'endo_inhib', 'NAD', 'PARG', 'base_fwd', 'base_rev', 'base_catalysis'
	params['PARP_2_PARG'] = 3
	params['time'] = 3
	P_to_G_concen = [.463, 1.852]
	init_parp = params['PARP']
	params['PARP'] = 0

	for ratio in P_to_G_concen:
		params['PARG'] = init_parp*ratio
'''

def hist():
	print("\nComparing two simulations using histogram.\n")
	# compares 2 runs, no averaging
	NADs = [1.0E+4,1.0E+5]
	labels = ['[NAD] = ' + str(NADs[0]), '[NAD] = ' + str(NADs[1])]

	all_params = []
	feature_names = ['size', 'branching ratio']

	shots = []
	data = {n:[] for n in feature_names}
	for i in rng(NADs):
		params['NAD'] = NADs[i]
		sshots = run_sim(deepcopy(params))
		sshot = sshots[-1] #get last one
		for feat in feature_names:
			data[feat] += [features.extract_one(feat, sshot)]
		all_params += [params]
		
	util.pickle_it(all_params, data) 

	print('final data=',data)

	plot.hist_first_and_last(data,params,feature_names, labels) # 1 img per feature




def sweep():
	# compares many parameters and averages each over many runs
	print("\nRunning parameter sweep with repeats.\n")
	NADs = [(5**i) for i in range(2,6)]
	#PARGs = [(10**i) for i in range(0,3)]
	#PARGs = [(10**i) for i in range(-10,-5)]
	
	all_params = []

	feature_names = ['size', 'branching ratio']

	stats = {'avg':[], 'std':[],'CI':[]}
	merged_data = {n:{'avg':deepcopy(stats), 'var':deepcopy(stats), 'sum':deepcopy(stats), 'max':deepcopy(stats), 'iod':deepcopy(stats),'1:2':deepcopy(stats)} for n in feature_names}


	shots = []
	for i in rng(NADs):
		params['NAD'] = NADs[i]
		print("[NAD] = ",NADs[i])
		#params['PARG'] = PARGs[i]
		#print("[PARG] = ",PARGs[i])
		#params['cut_rate'] = PARGs[i]
		#print("cut_rate = ",PARGs[i])
		repeats_data = {n:{'avg':[],'var':[], 'sum':[], 'max':[], 'iod':[],'1:2':[]} for n in feature_names}
		# Format: data[feature_name][stat]. Example: data['size']['avg']

		for r in range(params['repeats']):

			sshots = run_sim(deepcopy(params))
			sshot = sshots[-1] #get last one
			features.extract_stats(repeats_data, feature_names,sshot)

		features.merge_repeats(params,merged_data, repeats_data, feature_names)
		all_params += [params]
		
	util.pickle_it(all_params, merged_data) 

	plot.param_sweep(merged_data,params,NADs,'[NAD]',feature_names) #features * stats imgs
	#plot.param_sweep(merged_data,params,PARGs,'PARG rate',feature_names) #features * stats imgs


def time_series():
	print("\nRunning time series with repeats.\n")

	feature_names = ['size']

	stats = {'avg':[], 'std':[],'CI':[]}
	merged_data = [{n:{'avg':deepcopy(stats), 'var':deepcopy(stats), 'sum':deepcopy(stats), 'max':deepcopy(stats), 'iod':deepcopy(stats),'1:2':deepcopy(stats)} for n in feature_names} for t in range(params['num_snapshots'])]

	data = [{n:{'avg':[],'var':[], 'sum':[], 'max':[], 'iod':[],'1:2':[]} for n in feature_names} for t in range(params['num_snapshots'])]
	# Format: data[feature_name][stat]. Example: data['size']['avg']

	for r in range(params['repeats']):

		sshots = run_sim(deepcopy(params))
		if not len(sshots) == len(data):
			print('#sshots wrong! asked for %s, but got %s' %(len(sshots), len(data)))
			assert(False)
		for i in range(len(sshots)):
			features.extract_stats(data[i], feature_names,sshots[i])

	for i in range(len(data)):
		features.merge_repeats(params, merged_data[i], data[i], feature_names)
		
	util.pickle_it([params], merged_data) 

	plot.time_series(merged_data,params,feature_names,['sum']) 

###################################### KAPPY ###############################################

def run_sim(params):

	client = kappy.KappaStd()

	with open(params['model_file'], 'r') as file : 
		model = file.read()

	for name in params['species'].keys():
		val = params['species'][name]
		model = model.replace("init: _ " + name, "init: " + str(val) + " " + name)

	for name in params['variables'].keys():
		val = params['variables'][name]
		model = model.replace("var: '" + name + "' _", "var: '" + name + "' " + str(val))
 
	output_times = [t*params['time']/params['num_snapshots'] for t in range(1,params['num_snapshots']+1)]
	for t in output_times:
		model += '\n%mod: alarm ' +str(t) + ' do $SNAPSHOT "' + str(t) + '.ka";'
	#model = model.replace("mod: ([E] [mod] _ )=0", "mod: ([E] [mod] " + str(params['time']/params['num_snapshots']) + " )=0")
	with open(params['output_model_file'], 'w') as file : 
		file.write(model)


	client.add_model_string(model)
	client.project_parse()
	sim_params = kappy.SimulationParameter(pause_condition="[T] > " + str(params['time']),plot_period=params['time']/10)
	client.simulation_start(sim_params)
	client.wait_for_simulation_stop()
	results = client.simulation_plot()
	snaps = client.simulation_snapshots()

	iter_over = [i for i in range(params['num_snapshots'])]
	iter_over.reverse() #for some reason sshots are reverse sorted
	all_snaps  = [client.simulation_snapshot(snaps['snapshot_ids'][i]) for i in iter_over]

	#for i in rng(snaps['snapshot_ids']):
	#	snap  = client.simulation_snapshot(snaps['snapshot_ids'][i])
	#	if snap != []:
	#		break

	client.simulation_delete()
	client.shutdown()

	return all_snaps

main()