import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import seaborn as sns
sns.set(style="whitegrid")
import pandas as pd
import numpy as np
#plt.style.use('classic')
import os
import time
plt.rcParams.update({'font.size': 15})
plt.rcParams.update({'legend.fontsize': 15})
import pathlib


def makeIntervalGraph(adaptInTest, onlytrainingPhaseEval, intvls, allStimuli = False, allModels = False):
    modeText = 'training' if onlytrainingPhaseEval else 'globally'
    modeText += 'adaptInTest' if adaptInTest else 'notAdaptInTest'
    OnlyBD = 'All' if allStimuli else 'OnlyBD'
    overview = 'overview' if allModels else ''
    name = 'Bild4-prediction_success_in_time' + overview + 'Optimized' + modeText + OnlyBD
    fig, ax = plt.subplots(figsize=(13,10), num=name)
    count = 0
    for mode in ['training']:
        print(mode)
        intervals = {}
        fileIntvlCorrctness =str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/intvlsModCorrectnessPerModels" +str(adaptInTest) + str(onlytrainingPhaseEval) + str(intvls) + str(allStimuli)+str(allModels)+ ".csv" 
        first = True
        while os.stat(fileIntvlCorrctness).st_size == 0:
            print('waiting',os.stat(fileIntvlCorrctness).st_size , fileIntvlCorrctness)
            time.sleep(1)
        for line in open(fileIntvlCorrctness):
            if first:
                first = False
                continue
            l = line.split(',') 
            intervals[l[0].replace('RL-','RL_').replace('resc', 'Resc')] = l[1:]
        #print(intervals)
        for k in intervals.keys():
            x = []
            y = []
            if mode not in k:
                continue
            for a in range(len(intervals[k])):
                x.append(a)
            for i in intervals[k]:
                y.append(float(i))
            ax.plot(x,y, 'o-', label= k.split('ing')[1], markersize = 12)
            ax.set(ylim=(-0.05,1.05))
            ax.title.set_text('Prediction accuracy during training')
        ax.set_ylabel('prediction accuracy')
        count += 1
    plt.xlabel('progress of trials')
    #plt.subplots_adjust(right=0.7)
    ax.legend(ncol=2, numpoints=1, handler_map={tuple: HandlerTuple(ndivide=None)}, loc='lower left', bbox_to_anchor=(0, 0), prop={'size': 17})
    
    #plt.show()

    plt.savefig(str(pathlib.Path(__file__).parent.absolute()).split('benchmarks/')[0] + 'PlotImages/' + name +'vertical.png')



def makeBoxplots(adaptInTest, onlytrainingPhaseEval, allStimuli = False, allModels = False):
    #for tr in [True, False]:
        mode = '1-training' if onlytrainingPhaseEval else '2-globally'
        mode += 'adaptInTest' if adaptInTest else 'notAdaptInTest'
        OnlyBD = 'All' if allStimuli else 'OnlyBD'
        overview = 'overview' if allModels else ''
        while os.stat(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/swpl" +str(adaptInTest) + str(onlytrainingPhaseEval) +str(allStimuli)+str(allModels) +".csv").st_size == 0:
            time.sleep(1)
        fig, ax = plt.subplots(figsize=(15 if not allModels else 25,10), num='Bild' + overview + mode + 'Optimized' + OnlyBD)
        tips = pd.read_csv(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/swpl" +str(adaptInTest) + str(onlytrainingPhaseEval) +str(allStimuli)+str(allModels)+".csv")
        count = {}
        print('reading')
        for a in tips['id']:
            species = a.split('@')[1]
            if species not in count:
                count[species] = 0
            count[species] += 1
        sns.color_palette("Paired")
        ax = sns.swarmplot(x="mode", y="succ", hue="type", data=tips, size = 7)
        ax = sns.boxplot(x="mode", y="succ", data=tips, whis=np.inf,boxprops={'facecolor':'lightgrey', "linewidth" : 2},capprops={"linewidth" : 2}, medianprops={"linewidth" : 2}, whiskerprops={'linewidth':2},ax=ax)
        ax.set(ylim=(-0.05,1.05))
        plt.title('Model Parameters Optimized for Training Performance' if onlytrainingPhaseEval else 'Model Parameters Optimized for Overall Performance')
        plt.ylabel('prediction accuracy')
        plt.xlabel('model')
        plt.rc('xtick', labelsize=17) 

        ax.set_xticklabels([a.get_text().replace('-', '\n').replace('s\nM','sM') for a in ax.get_xticklabels()], rotation=45, horizontalalignment='center')
        current_handles, current_labels = plt.gca().get_legend_handles_labels()

        reversed_handles = list(current_handles)
        reversed_labels = [a + ' (N = ' + str(int(count[a]/len(ax.xaxis.get_ticklabels()))) + ')' for a in current_labels if a in count.keys()]
        #plt.subplots_adjust(right=0.7)
        plt.legend(reversed_handles,reversed_labels,ncol=2, numpoints=1, handler_map={tuple: HandlerTuple(ndivide=None)}, loc='lower right', bbox_to_anchor=(1, 0))
        #fig.subplots_adjust(bottom=0.18, top = 0.94, right= 0.75 if not allModels else 0.85, left = 0.1 if not allModels else 0.04) 
        fig.subplots_adjust(bottom=0.18, top = 0.94, right= 0.95 if not allModels else 0.95, left = 0.1 if not allModels else 0.04) 
        #plt.show()
        print('saving')
        plt.savefig(str(pathlib.Path(__file__).parent.absolute()).split('benchmarks/')[0] + 'PlotImages/Bild' + overview + mode + 'Optimized' + OnlyBD + '.png')