'''
Support functions handling data import and formatting for plotting
'''

import pandas as pd
from pprint import pprint
from collections import namedtuple

def import_plot_data(file_path):
    '''
    Imports raw data from the Excel template file and returns:
    1) Formatted data for waterfall plotting
    2) Formatted data for spider plotting
    3) Formatted data for swimmer plotting
    '''
    xl = pd.ExcelFile(file_path)
    
    df_waterfall_data = xl.parse('Waterfall_data')
    df_spider_data = xl.parse('Spider_data')
    df_swimmer_data = xl.parse('Swimmer_data_days')
    data_set = {}


    data_set['waterfall_data'] = parse_df_waterfall(df_waterfall_data)
    #spider_data = parse_df_spider(df_spider_data)
    data_set['swimmer_data'] = parse_df_swimmer(df_swimmer_data)

    return data_set

def parse_df_swimmer(df_swimmer_data):
    '''
    Parse dataframe of swimmer plot data and extract dates and events
    '''
    pprint(df_swimmer_data)
    #Sort df_swimmer_data by their totals
    numcols = len(list(df_swimmer_data)) #number of keys
    numpatients = len(df_swimmer_data.ix[:,0])

    list_of_lengths = []
    for row in range(numpatients):
        pt_sum = 0
        for col in range(1,numcols):
            val =  df_swimmer_data.ix[row,col]
            if val.isnumeric():
                pt_sum+=dval
        list_of_lengths.append(pt_sum)
    print(list_of_lengths)

    return 1

    # swimmer_headers = list(df_swimmer_data)
    # swimmer_data = {}
    # for header in swimmer_headers:
    #     swimmer_data[header] = df_swimmer_data[header]

    # swimmer_data = []
    # for key in list(df):
    #     swimmer_data.append(df[key])
    # pt_list = swimmer_data[0] #list of the patients
    # pt_stacks = swimmer_data[1:] #their corresponding 'stacks', each col is a dosage level (if applicable)

def parse_df_waterfall(df_waterfall_data):
    '''
    Prepare waterfall plot data for plotting
    '''
    #standard columns (always present first 4 columns & in this order) are: 'Patient number', 'Best response percent change', 'Patient response', 'Cancer'
    #all columns after these first 4 are custom (related to a table shown below the plot, col headers are the table row labels)
    df_waterfall_data = df_waterfall_data.sort_values('Best response percent change', ascending = False)
    return df_waterfall_data.fillna(value=None,)

    # waterfall_data = []
    # for key in list(df_waterfall_data):
    #     waterfall_data.append(df_waterfall_data[key])
    # return waterfall_data

def parse_df_spider(df_spider_data):
    spider_headers = list(df_spider_data)
    spider_data = {}
    for header in spider_headers:
        spider_data[header] = df_spider_data[header]