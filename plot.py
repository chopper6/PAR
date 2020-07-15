import matplotlib.pyplot as plt, util, math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LogNorm #SymLogNorm if need
from matplotlib import rcParams
import numpy as np
from util import rng


COLORS = ['green','red','blue','purple','cyan','orange','brown','magenta','yellow','grey']
MARKERS = ['o', '^','D']
plt.rcParams["font.family"] = "serif"


def hist_first_and_last(data, params, feature_names, labels):
	for feature in feature_names:
		x1,x2 = data[feature][0],data[feature][-1]
		fig = plt.figure(figsize=(12,8))
		plt.hist(x1, facecolor='red', alpha=0.5) #normed=1 
		plt.hist(x2, facecolor='blue', alpha=0.5) #normed=1 
		plt.legend(labels, fontsize=20)

		finish_plot(params,'histo_' + feature, feature,'counts')


def param_sweep_one(Y, params, variable_values, title, xlabel, ylabel, loglog=True):
	#print("\nPLOT for %s \n Y, variable_values" %ylabel, Y, variable_values)
	#print("Yavg: ", Y['avg'])
	fig = plt.figure(figsize=(12,8))
	y_avg = Y['avg']
	if not params['use_CI']:
		top, btm = np.add(Y['avg'],Y['std']), np.subtract(Y['avg'],Y['std'])
	else:
		top, btm = Y['CI'][1], Y['CI'][0]

	if loglog:
		plt.loglog(variable_values,y_avg,alpha=.8, linewidth=2, color='blue')
	else:
		plt.plot(variable_values,y_avg,alpha=.8, linewidth=2, color='blue')
	
	plt.fill_between(variable_values,top,btm,alpha=.2, color='blue')

	finish_plot(params,'param_sweep_' + title, xlabel, ylabel)


def param_sweep(data, params, variable_values, variable_name, feature_names):
	for feature in feature_names:
		for metric in data[feature].keys():
			title, ylabel = variable_name + '_x_' + '_' + feature + '_' + metric, feature + '_' + metric
			param_sweep_one(data[feature][metric], params, variable_values, title, variable_name, ylabel)


def time_series(data,params,feature_names, metrics):
	for feature in feature_names:
		for metric in metrics:
			assert(metric in data[0][feature].keys()) #if error, metric is not calculated in features.extract_stats()
			title, ylabel = feature + '_' + metric, feature + '_' + metric
			time_series_one(data,feature,metric, params, title, feature, loglog=False)

def time_series_one(data, feature,metric, params, title, ylabel,loglog=False):
	#print("\nPLOT for %s \n Y, variable_values" %ylabel, Y, variable_values)
	#print("Yavg: ", Y['avg'])
	X = [(i+1)*params['time']/params['num_snapshots'] for i in range(params['num_snapshots'])]
	Y_avg = [data[i][feature][metric]['avg'] for i in range(params['num_snapshots'])]
	fig = plt.figure(figsize=(12,8))

	if not params['use_CI']:
		Y_std = [data[i][feature][metric]['std'] for i in range(params['num_snapshots'])]
		top, btm = np.add(Y_avg,Y_std), np.subtract(Y_avg,Y_std)
	else:
		top, btm = Y['CI'][1], Y['CI'][0]

	if loglog:
		plt.loglog(X,Y_avg,alpha=.8, linewidth=2, color='blue')
	else:
		plt.plot(X,Y_avg,alpha=.8, linewidth=2, color='blue')
	
	plt.fill_between(X,top,btm,alpha=.2, color='blue')

	finish_plot(params,'Time_series_' + title, 'Time', ylabel)



def finish_plot(params, title, xlabel, ylabel):

	plt.xlabel(xlabel, fontsize=20)
	plt.ylabel(ylabel, fontsize=20)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)

	if params['write_params_on_img']: 
		ax = plt.gca()
		cut = 80
		plt.title('Parameters: ' + str(params)[:cut] + '\n' + str(params)[cut:2*cut] 
			+ '\n' + str(params)[2*cut:3*cut] + '\n' + str(params)[3*cut:],fontsize=10)
	#else:
	#	plt.title(title,fontsize=18) 
	#fig.tight_layout()
	
	if params['save_fig']:
		title = params['out_dir']+title+'_'+params['timestamp']+'.png'
		plt.savefig(title,dpi=params['dpi'])
	else:
		plt.show()
	plt.clf()
	plt.cla()
