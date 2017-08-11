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
    numcols = len(list(df_swimmer_data)) #number of keys
    numpatients = len(df_swimmer_data.ix[:,0])

    list_of_lengths = []
    for row in range(numpatients):
        pt_dose_lengths = [x for x in df_swimmer_data.ix[row,1:numcols-1] if pd.notnull(x)]
        pt_sum = sum(pt_dose_lengths)
        list_of_lengths.append(pt_sum)
    df_swimmer_data['Sum'] = list_of_lengths
    df_swimmer_data = df_swimmer_data.sort_values('Sum',ascending = False) #sort largest to smallest
    df_swimmer_data.ix[:,1:] = df_swimmer_data.ix[:,1:].fillna(0)
    print(df)
    return df_swimmer_data

def parse_df_waterfall(df_waterfall_data):
    '''
    Prepare waterfall plot data for plotting
    '''
    #standard columns (always present first 4 columns & in this order) are: 'Patient number', 'Best response percent change', 'Patient response', 'Cancer'
    #all columns after these first 4 are custom (related to a table shown below the plot, col headers are the table row labels)
    df_waterfall_data = df_waterfall_data.sort_values('Best response percent change', ascending = False)
    return df_waterfall_data

def parse_df_spider(df_spider_data):
    spider_headers = list(df_spider_data)
    spider_data = {}
    for header in spider_headers:
        spider_data[header] = df_spider_data[header]