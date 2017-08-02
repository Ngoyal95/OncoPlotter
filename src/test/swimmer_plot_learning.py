#1 python3

#Testing matplotlib to understand how to make a swimmer plot
''' 
Refs:
Markers: https://codeyarns.com/2013/10/24/markers-of-matplotlib/
Axes documentation: https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot
Drawing an arrow: https://philbull.wordpress.com/2012/04/05/drawing-arrows-in-matplotlib/
Scatter plot with different markers: https://stackoverflow.com/questions/26490817/matplotlib-scatter-plot-with-different-markers-and-colors

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
        (5.1,'g',[[3,'^'],[4,'^']]),
        (7, 'r',[[3,'^'],[6,'^']]),
        (3, 'b',[[1,'^'],[2.9,'^']])
        ]

def unpack_swimmer_values(dataset):
    n = len(ex_set) #number of bars, will be needed when arranging them
    bar_locations = np.arange(n) #evenly spaced locations of the bars, list [0 1 ........ n-1]

    dataset.sort(key=lambda tup: tup[0]) #sort in place by the legnth of response bar, ascending order

    #now get lists of everything in same order as the sorted dataset
    bar_lengths = [val[0] for val in dataset]
    bar_keys = [val[1] for val in dataset] #gets bar colors in same order
    bar_events = [val[2] for val in dataset]

    i = 0
    event_x = []
    event_y = []
    event_type = []
    for event_for_bar in bar_events:
        #now have list of list of events for one bar
        for event in event_for_bar:
            event_x.append(event[0])
            event_y.append(i)
            event_type.append(event[1])
        i+=1


    return bar_lengths, bar_keys, event_x, event_y, event_type, bar_locations
    
if __name__ == '__main__':
    bar_lens, bar_keys, event_x, event_y, event_type, bar_locations = unpack_swimmer_values(ex_set)
    markersize = 10 #needs to be user variable so that as more/less bars added, it looks ok
    fig, ax = plt.subplots()

    #plotting the bars
    ax.barh(bar_locations, bar_lens, color = bar_keys) #plot horizontal bar graph
    #ax.bar() would make regular bar graph, would want to arrange data in decreasing order for waterfall

    #testing with list of points
    # li = [(5,5),(4,3),(6,1)]
    # mark = [u'^',u'x',u'^']
    # col = ['r','b','g']
    # xloc, yloc = zip(*li) #unpack coords into X and Y lists for plotting

    print(list(zip(event_type,'k',event_x,event_y)))

    for s,x,y in zip(event_type,event_x,event_y):
        plt.plot(x,y,marker=s,markersize=markersize)

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



