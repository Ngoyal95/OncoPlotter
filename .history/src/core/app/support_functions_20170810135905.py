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
    df_swimmer_data = xl.parse('Swimmer_data')
    data_set = {}
    
    waterfall_data = parse_df_waterfall(df_waterfall_data)
    #spider_data = parse_df_spider(df_spider_data)
    #swimmer_data = parse_df_swimmer(df_swimmer_data)

    return waterfall_data

def parse_df_swimmer(df):
    '''
    Parse dataframe of swimmer plot data and extract dates and events
    '''

    #Sort df_swimmer_data by their totals
    numcols = len(list(df)) #number of keys


    # swimmer_headers = list(df_swimmer_data)
    # swimmer_data = {}
    # for header in swimmer_headers:
    #     swimmer_data[header] = df_swimmer_data[header]

    swimmer_data = []
    for key in list(df):
        swimmer_data.append(df[key])
    pt_list = swimmer_data[0] #list of the patients
    pt_stacks = swimmer_data[1:] #their corresponding 'stacks', each col is a dosage level (if applicable)

def parse_df_waterfall(df_waterfall_data):
    '''
    Prepare waterfall plot data for plotting
    '''
    #standard columns (always present first 4 columns & in this order) are: 'Patient number', 'Best response percent change', 'Patient response', 'Cancer'
    #all columns after these first 4 are custom (related to a table shown below the plot, col headers are the table row labels)
    df_waterfall_data = df_waterfall_data.sort_values('Best response percent change', ascending = False)
    
    # waterfall_headers = list(df_waterfall_data) #use to create seperate lists stored in a dict, keys are names of col headers
    # waterfall_data = {}
    # for header in waterfall_headers:
    #     waterfall_data[header] = df_waterfall_data[header]
    # return waterfall_data

    return [df_waterfall_data]

    # waterfall_data = []
    # for key in list(df_waterfall_data):
    #     waterfall_data.append(df_waterfall_data[key])
    # return waterfall_data

def parse_df_spider(df_spider_data):
    spider_headers = list(df_spider_data)
    spider_data = {}
    for header in spider_headers:
        spider_data[header] = df_spider_data[header]