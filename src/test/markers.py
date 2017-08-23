#!/usr/bin/env python

import matplotlib.pyplot as pyplot

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

def line_plot():

    x_list = [1]
    y_list = [1]

    pyplot.clf()
    for mark in mark_dict:
        y_list = [y_val + 10 for y_val in y_list]
        pyplot.plot(x_list, y_list, label=mark_dict[mark], marker=mark)

    pyplot.legend(loc="best", prop={'size':11})
    pyplot.savefig("markers.png")
    pyplot.show()

def main():
    line_plot()

if "__main__" == __name__:
    main()