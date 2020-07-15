import util, plot
from util import rng
import numpy as np, scipy.stats as st

DEBUG = True

################################ EXTRACTING KAPPA SNAPSHOT ######################################


def get_branch_number(graph) :
    counter = 0
    for agent in graph[1] :
        for node_site in agent['node_sites']:
            if node_site['site_name'] == 'branch' and node_site['site_type'][1]['port_links'] :
                #if branch site is not empty
                counter +=1
    return counter

def get_features(snap) :
    graphs = snap['snapshot_agents']
    infos = [] 
    for graph in graphs : #run through the graphs
        # if size of graph is 1 should catch all of this:
        # ignores if PARG or PARP bound at end, but v minor effect

        #if graph[1][0]['node_type'] == 'PARG' :
        #   continue
        info = {}

        size = len(graph[1])
        if size > 1:
            info['size'] = len(graph[1]) # number of agents
            info['number'] = graph[0] #number of that kind of graph
            info['branching ratio'] = get_branch_number(graph)/info['size']
            
            for i in range(int(info['number'])):
                infos += [info]


    return infos




################################# ORGANIZING DATA ##################################

def extract_one(name, sshot):
    data = get_features(sshot)
    feat = [data[i][name] for i in rng(data)] # if error, feature name is not recognized
    return feat

def extract_stats(data, feature_names, sshot):
    for name in feature_names:
        feat = extract_one(name, sshot)
        if feat != []:

            data[name]['avg'] += [util.avg(feat)]
            data[name]['var'] += [util.var(feat)]
            data[name]['sum'] += [sum(feat)]
            if util.avg(feat) != 0:
                iod = util.var(feat)/util.avg(feat)
            else:
                iod = 0
            data[name]['iod'] += [iod]
            max1 = max(feat)
            data[name]['max'] += [max1]
            if len(feat)<=1:
                data[name]['1:2'] += [0]
            else:
                feat.remove(max1)
                max2 = max(feat)

                if max1==0:
                    ratio = 0
                else: 
                    ratio = (max1 - max2)/max1
                data[name]['1:2'] += [ratio]
                #print("DATA %s" %(name), data[name])


def merge_repeats(params, merged_data, repeats_data, feature_names):
    for name in feature_names:
        for metric in repeats_data[name].keys():

            #merged_data[name][metric]['avg'] = util.avg(repeats_data[name][metric])

            a = np.array(repeats_data[name][metric])
            if a.size != 0:
                mean = np.mean(a)
                std = np.std(a)
            else:
                mean, std = 0,0

            merged_data[name][metric]['avg'] += [mean]
            merged_data[name][metric]['std'] += [std]
            #print('avg, std', merged_data[name][metric]['avg'],merged_data[name][metric]['std'],a,'\n')

            if params['use_CI']:

                if params['std_devs']==1:
                    conf_interval = st.t.interval(0.68, len(a)-1, loc=mean, scale=st.sem(a)) #1 standard devs
                elif params['std_devs']==2:
                    conf_interval = st.t.interval(0.95, len(a)-1, loc=mean, scale=st.sem(a)) #2 standard devs
                elif params['std_devs']==3:
                    conf_interval = st.t.interval(0.997, len(a)-1, loc=mean, scale=st.sem(a)) #3 standard devs
                else:
                    assert(False)

                merged_data[name][metric]['CI'] = conf_interval
                '''
                intervals, stats = [conf_interval1, conf_interval2, conf_interval3], [['top1','btm1'],['top2','btm2'],['top3','btm3']]
                for i in util.rng(intervals):
                    interval, stat = intervals[i], stats[i]
                    a_trimd=[]
                    for ele in a:
                        if ele > interval[0] and ele < interval[1]:
                            a_trimd+=[ele] 

                    if np.count_nonzero(a_trimd) == 0:
                        conf_min, conf_max = 0,0
                    else:
                        conf_min, conf_max = min(a_trimd), max(a_trimd)
                    merged_data[name][metric][stat[0]] += [conf_max]
                    merged_data[name][metric][stat[1]] += [conf_min]

                #print('features:',metric,merged_data[name][metric])
                '''


