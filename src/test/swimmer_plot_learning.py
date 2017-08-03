#1 python3

#Testing matplotlib to understand how to make a swimmer plot
''' 
Refs:
Markers: https://codeyarns.com/2013/10/24/markers-of-matplotlib/
Axes documentation: https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot
Drawing an arrow: https://philbull.wordpress.com/2012/04/05/drawing-arrows-in-matplotlib/
Scatter plot with different markers: https://stackoverflow.com/questions/26490817/matplotlib-scatter-plot-with-different-markers-and-colors
Stylesheet reference: http://www.futurile.net/2016/02/27/matplotlib-beautiful-plots-with-style/

'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

'''
packaging swimmer plot data:
[(), (),...,(end_date, bar_key, [(date,event),....,(date,event)]),...()]
'''

# ex_set = [
#         (5.1,'g',[[3,'CR'],[4,'PD']]),
#         (7, 'r',[[3,'PD'],[7,'OS']]),
#         (3, 'b',[[1,'CR'],[2.9,'OS']])
#         ]

ex_set = [
        (5.1,'#7ad3f0',[[3,'PR'],[4,'CR']]),
        (7, '#7ad3f0',[[3,'PD'],[6,'EOT']]),
        (3, '#7ad3f0',[[1,'PR'],[2.9,'EOT']])
        ]
def map_markers(event_type,plot_type):
    '''
    Based on event type, maps to the correct marker and marker color.
    Unless user updates plot settings, will use the std_indic_dict for indicators, and std_bar_keys_dict for bar color coding.
    plot_type = 0 means this is regular swimmer, not tracking dosages. plot_type = 1 means stacked barplot with dosages
    '''
    std_indic_dict = {
                'CR': ['^','#296cdb'],
                'PR': ['^','#ffee22'],
                'PD': ['x','#353835'],
                'EOT': ['1','#000000']
                }
    e_m = []
    e_c = []
    for event in event_type:
        e_m.append(std_indic_dict[event][0])
        e_c.append(std_indic_dict[event][1])

    return e_m, e_c

def unpack_swimmer_values(dataset,plot_type):
    '''
    Unpacks the swimmer plot data delivered from the UI into a form that the plotter can use.
    Type indicates if stacked bars are being used (which indicate multiple types of drug dosages). 
    plot_type = 0 means regular swimmer, no drug dosage spec. plot_type = 1 means dosage swimmer.
    '''
    if plot_type == 0:
        n = len(dataset) #number of bars, will be needed when arranging them
        bar_locations = np.arange(n) #evenly spaced locations of the bars, list [0 1 ........ n-1]

        dataset.sort(key=lambda tup: tup[0]) #sort in place by the legnth of response bar, ascending order

        #now get lists of everything in same order as the sorted dataset
        bar_lengths = [val[0] for val in dataset]
        bar_keys = [val[1] for val in dataset] #gets bar colors in same order
        bar_events = [val[2] for val in dataset]

        i = 0
        event_x = [] #x-axis locations of events
        event_y = [] #y-axis location of events
        event_type = [] #the event type (CR,PR,PD,EOT,etc...)
        for event_for_bar in bar_events:
            #now have list of list of events for one bar
            for event in event_for_bar:
                event_x.append(event[0])
                event_y.append(i)
                event_type.append(event[1])
            i+=1
        
        event_markers, event_colors = map_markers(event_type,0)

        return bar_lengths, bar_keys, event_x, event_y, event_markers, event_colors, bar_locations
    else:
        pass
    
if __name__ == '__main__':
    bar_lengths, bar_keys, event_x, event_y, event_markers, event_colors, bar_locations = unpack_swimmer_values(ex_set,0)
    markersize = 20 #needs to be user variable so that as more/less bars added, it looks ok
    bar_width = 0.75
    
    fig, ax = plt.subplots()
    plt.style.use('fivethirtyeight') #style of plot, ggplot also good

    #plotting the bars
    ax.barh(bar_locations, bar_lengths, bar_width, color = bar_keys) #plot horizontal bar graph
    ax.barh(bar_locations, [1,2,3], bar_width, left = bar_lengths) #stack bars on top
    
    #ax.bar() would make regular bar graph, would want to arrange data in decreasing order for waterfall

    #testing with list of points
    # li = [(5,5),(4,3),(6,1)]
    # mark = [u'^',u'x',u'^']
    # col = ['r','b','g']
    # xloc, yloc = zip(*li) #unpack coords into X and Y lists for plotting

    #print(list(zip(event_type,'k',event_x,event_y)))

    for m,c,x,y in zip(event_markers,event_colors,event_x,event_y):
        plt.plot(x,y,marker=m,markersize=markersize,c=c)

    #drawing arrows
    #arrow(x,y,dx,dy,**kwargs)
    # for i in range(len(data)):
    #     plt.arrow(data[i],bar_locations[i],0.25,0,fc="k",ec="k",head_width=0.4,head_length=0.3)

    plt.title('Swimmer Plot')
    plt.xlabel('Weeks from baseline')
    plt.ylabel('Patients')
    plt.show()

    '''
    n = 5 #number of bars
    data = np.array(range(n)) + np.random.rand(n) #need to arrange data in increasing order

    fig, ax = plt.subplots()

    #drawing vertical lines
    plt.axvline(x=2, linestyle='--', c='k', alpha = 0.5) #black line, dashed

    #plotting the bars
    bar_colors = ['r','r','g','g','b']
    bar_locations = np.arange(n) #[0 1 2 3 4]
    ax.bar(bar_locations, data, color = bar_colors) #plot horizontal bar graph
    #ax.bar() would make regular bar graph, would want to arrange data in decreasing order for waterfall

    #plotting a circle
    ax.plot(3,1,'r+',markersize = markersize) #plots a red + at x=3,y=1 (on 1st bar)
    ax.plot(3,5,'r^',markersize = markersize)
    
    #testing with list of points
    li = [(5,5),(4,3),(6,1)]
    mark = [u'^',u'x',u'^']
    col = ['r','b','g']
    xloc, yloc = zip(*li) #unpack coords into X and Y lists for plotting

    for s,c,x,y in zip(mark,col,xloc,yloc):
        plt.plot(x,y,marker=s,c=c,markersize=markersize)

    #drawing arrows
    #arrow(x,y,dx,dy,**kwargs)
    # for i in range(len(data)):
    #     plt.arrow(data[i],bar_locations[i],0.25,0,fc="k",ec="k",head_width=0.4,head_length=0.3)

    plt.title('Swimmer Plot')
    plt.xlabel('Weeks from baseline')
    plt.ylabel('Patients')
    plt.show()
    '''



