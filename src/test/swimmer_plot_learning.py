#1 python3

"""
Refs:
Markers: https://codeyarns.com/2013/10/24/markers-of-matplotlib/
Axes documentation: https://matplotlib.org/api/axes_api.html
Labels above bars: https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart
Drawing an arrow: https://philbull.wordpress.com/2012/04/05/drawing-arrows-in-matplotlib/
Arrow docs: https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.arrow.html
Scatter plot with different markers: https://stackoverflow.com/questions/26490817/matplotlib-scatter-plot-with-different-markers-and-colors
Stylesheet reference: http://www.futurile.net/2016/02/27/matplotlib-beautiful-plots-with-style/

Hex colors: https://www.w3schools.com/colors/colors_hexadecimal.asp
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pprint import pprint
import pandas as pd
import itertools

mark_dict = {
".":"point",
",":"pixel",
"o":"circle",
"v":"triangle_down",
"^":"triangle_up",
"<":"triangle_left",
">":"triangle_right",
"1":"tri_down",
"2":"tri_up",
"3":"tri_left",
"4":"tri_right",
"8":"octagon",
"s":"square",
"p":"pentagon",
"*":"star",
"h":"hexagon1",
"H":"hexagon2",
"+":"plus",
"D":"diamond",
"d":"thin_diamond",
"|":"vline",
"_":"hline"
}

ex_stack_base = [
                [10,'b'],
                [7, '#7ad3f0'],
                [3, '#7ad3f0']
                ]   

ex_stack_1 = [
            [2,'k'],
            [1.5,'k'],
            [6,'k']
            ]

ex_stack = [ex_stack_base,ex_stack_1]
ex_events = [
            [[3,'PR'],[4,'CR']],
            [[3,'PD'],[6,'EOT']],
            [[1,'PR'],[2.9,'EOT']]
            ]

def pull_from_spreadsheet():
    file_path = r'C:\Users\goyaln2\Desktop\ex_swimmer_data.xlsx'
    xl = pd.ExcelFile(file_path)
    df = xl.parse()

    stks = []
    for key in list(df):
        stks.append(df[key])
    labels = stks[0]
    stks = stks[1:]
    
    stks[0] = [list(l) for l in zip(stks[0],['#7ad3f0']*len(stks[0]))]
    stks[1] = [list(l) for l in zip(stks[1],['#fc8238']*len(stks[1]))]
    stks[2] = [list(l) for l in zip(stks[2],['#78797a']*len(stks[2]))]
    evnts = list(itertools.repeat([[300,'CR']],len(stks[0])))
    return(labels,stks,evnts)
    ### Format of the stks variable has to be [[], [], []] (at least one nested list)

def map_markers(event_type):
    '''
    Based on event type, maps to the correct marker and marker color.
    Unless user updates plot settings, will use the std_indic_dict for indicators, and std_bar_keys_dict for bar color coding.
    '''
    std_indic_dict = {
                'CR': ['^','#296cdb'],
                'PR': ['^','#ffee22'],
                'PD': ['x','#353835'],
                'EOT': ['1','#000000'],
                None: ['','None']
                }
                
    std_bar_keys_dict = {}

    e_m = []
    e_c = []
    for event in event_type:
        e_m.append(std_indic_dict[event][0])
        e_c.append(std_indic_dict[event][1])

    return e_m, e_c

def unpack_swimmer_values(stacks, events):
    '''
    Unpacks the swimmer plot data delivered from the UI into a form that the plotter can use.
    Type indicates if stacked bars are being used (which indicate multiple types of drug dosages). 
    plot_type = 0 means regular swimmer, no drug dosage spec. plot_type = 1 means dosage swimmer.
    '''
    n = len(stacks[0]) #number of pts, will be needed when arranging the bars
    bar_locations = np.arange(n) #evenly spaced locations of the bars, list [0 1 ........ n-1]
    
    length_of_each_stack = [] #list of total length of each stack, used for sorting
    for i in range(n):
        #each pt
        pt_bar_len = 0
        for j in range(len(stacks)):
            #number of stacks
            pt_bar_len += stacks[j][i][0] #access length in each stack for a pt
        length_of_each_stack.append(pt_bar_len)

    stacks_zipped = zip(*stacks)
    stacks_zipped_with_events = zip(stacks_zipped,events)
    length_stacks_events = zip(length_of_each_stack,stacks_zipped_with_events)
    sorted_together = sorted(length_stacks_events)
    length_of_each_stack,stacks_zipped_with_events = zip(*sorted_together)
    stacks_zipped,events = zip(*stacks_zipped_with_events)
    stacks = list(zip(*stacks_zipped))
    
    #now have stacks and events sorted in ascending order, ready for plotting
    stack_length_lists = []
    stack_color_lists = []
    for i in range(len(stacks)):
        indiv_stack_length = []
        indiv_stack_color = []
        for j in range(len(stacks[i])):
            indiv_stack_length.append(stacks[i][j][0])
            indiv_stack_color.append(stacks[i][j][1])
        stack_length_lists.append(indiv_stack_length)
        stack_color_lists.append(indiv_stack_color)
    
    i = 0
    event_x = [] #x-axis locations of events
    event_y = [] #y-axis location of events
    event_type = [] #the event type (CR,PR,PD,EOT,etc...)
    for event_for_bar in events:
        #now have list of list of events for one bar
        for event in event_for_bar:
            event_x.append(event[0])
            event_y.append(i)
            event_type.append(event[1])
        i+=1
    event_markers, event_colors = map_markers(event_type)

    return bar_locations, stack_length_lists, stack_color_lists, event_x, event_y, event_markers, event_colors

if __name__ == '__main__':
    labels,stk,evnts = pull_from_spreadsheet()
    bar_locations, stack_length_lists, stack_color_lists, event_x, event_y, event_markers, event_colors = unpack_swimmer_values(stk, evnts)    
    markersize = 5 #needs to be user variable so that as more/less bars added, it looks ok
    bar_width = 0.75
    
    fig, ax = plt.subplots()
    plt.style.use('fivethirtyeight') #style of plot, ggplot also good

    #plotting the bars
    offset_list = [0]*len(stack_length_lists[0])
    for i in range(len(stack_length_lists)):
        ax.barh(bar_locations, stack_length_lists[i], bar_width, color = stack_color_lists[i], left = offset_list, edgecolor = 'k') #stack bars on top
        offset_list = [sum(x) for x in zip(offset_list, stack_length_lists[i])]

    #ax.set_yticklabels(labels)
           
    for m,c,x,y in zip(event_markers,event_colors,event_x,event_y):
        plt.plot(x,y,marker=m,markersize=markersize,c=c)

    # Legend
    dose1 = mpatches.Patch(color = '#7ad3f0', label = '60mg')
    dose2 = mpatches.Patch(color = '#fc8238', label = '40mg')
    dose3 = mpatches.Patch(color = '#78797a', label = '20mg')
    plt.legend(handles=[dose1,dose2,dose3])
    
    plt.axvline(x=365, linestyle = '--', alpha = 0.5, c = 'k',linewidth = 1)

    #drawing arrows
    #arrow(x,y,dx,dy,**kwargs)
    for i in range(len(offset_list)):
        plt.arrow(offset_list[i]+0.05,bar_locations[i],5,0,fc="k",ec="k",head_width=0.6,head_length=5,width = 0.4)

    plt.title('Duration of treatment by dose')
    plt.xlabel('Time from randomization (days)')
    plt.ylabel('Patients treated with Cabozantinib')
    #plt.grid()
    plt.show()