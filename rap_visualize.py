# FILE: rap_visualize.py.py
# WRITER:lee matan,leem72,207378803
# EXERCISE:intro2cse rap_Lee 2020
# DESCRIPTION:
# NOTES:


import pandas as pd
from matplotlib import pyplot as plt
import json

def

def create_one_year_dt(dt, col, v):
    '''

    :param dt: the full data document, csv
    :param col: the category we want to choose one value to show from.
    :param v: the value of the column for whom we want to show instances (lines)
    :return: a data frame of all the samples of the same value of the column we chose.
    '''
    full_data = pd.read_csv('dt')
    v_dt = full_data[full_data.col == v]
    return v_dt


def strings_col_into_dicts_col(col, lst):
    '''
    A function that turns the a columns of a csv to a list of dictionaries
    :param col: a col of a csv Data Frame
    :param lst: an empty list
    :return: a list of dictionaries
    '''
    for profs in col:
        s = profs.replace("'", "\"")
        d = json.loads(s)
        lst.append(d)
    return lst


def find_popular_prof_per_year(lst, dict):

    return (year, most_popular_prof, total_performances)


if __name__ == '__main__':
