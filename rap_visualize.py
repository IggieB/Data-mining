# FILE: rap_visualize.py.py
# WRITER:lee matan,leem72,207378803
# EXERCISE:intro2cse rap_Lee 2020
# DESCRIPTION:
# NOTES:


import pandas as pd
from matplotlib import pyplot as plt
import json
from natsort import natsorted


def create_dt_years_lst(dt):
    years_lst = []
    data = pd.read_csv(dt)
    relevant_data = data.Date  # not general, refers only to Date called column
    for line in relevant_data:
        if line in years_lst:
            continue
        years_lst.append(line)
    ordered_years_lst = natsorted(years_lst)
    return ordered_years_lst


def create_one_year_dt(dt, v):
    '''

    :param col_name:
    :param dt: the full data document, csv
    :param col: the category we want to choose one value to show from.
    :param v: the value of the column for whom we want to show instances (lines)
    :return: a data frame of all the samples of the same value of the column we chose.
    '''
    full_data = pd.read_csv(dt)
    v_dt = full_data[full_data.Date == v] # not general, refers only to Date
    # called column
    return v_dt


def strings_col_into_dicts_col(col_dt, lst):
    '''
    A function that turns the a columns of a csv to a list of dictionaries
    :param col_dt: a col of a csv Data Frame
    :param lst: an empty list
    :return: a list of dictionaries
    '''
    # if col_dt.empty:
    #     return lst
    for d in col_dt:
        # if not d:
        #     lst.append('None')
        #     continue
        s = d.replace("'", "\"")
        d = json.loads(s)
        lst.append(d)
    return lst


def find_popular_prof(lst):
    '''

    :param lst: a list of dictionaries
    :return: a tuple of most popular word of the year, and the number of its
    performances .
    '''
    if not lst:
        return 'no profanities', 'yes'
    d = lst[0]
    for dic in lst[1:]:
        for key, value in dic.items():
            if key in d:
                d[key] += value
            else:
                d[key] = value
    profs_list = list(d.keys())
    frequencies = list(d.values())
    max_value = max(frequencies)
    index_of_frequency = frequencies.index(max_value)
    most_popular_prof = profs_list[index_of_frequency]
    year_popular = most_popular_prof, max_value
    return year_popular


def find_popular_prof_per_year(dt, lst):
    '''

    :param dt: full data csv file
    :param lst: a list of the column values we want to find data information about. (years)
    :return:
    '''
    popular_profs_dict = {}
    for year in lst:
        year_dt = create_one_year_dt(dt, year)
        profs_dicts_lst = strings_col_into_dicts_col(year_dt.Profanities, [])
        popular_prof_info = find_popular_prof(profs_dicts_lst)
        popular_profs_dict[year] = popular_prof_info
    return popular_profs_dict


def initiate_popular_prof_of_year_df(dic):
    lst_x = ['{}: {}'.format(key, value[0]) for key, value in dic.items()]
    lst_y = [value[1] for value in dic.values()]
    return lst_x, lst_y


def create_df_rows(dic):
    l = []
    for key, value in dic.items():
        l.append([key, value[0], value[1]])
    return l


def create_df_popular_prof_per_year(lst, columns):
    df = pd.DataFrame(lst, columns=columns)
    # print(df)
    plt.bar(df.year, df.frequency)
    plt.show()
    return df


if __name__ == '__main__':
    rap_full_data = 'rap_sample_years.csv'
    years = create_dt_years_lst(rap_full_data)
    d = find_popular_prof_per_year(rap_full_data, years)
    l_of_lsts = create_df_rows(d)
    columns = ['year', 'most_popular_profanity', 'frequency']
    print(l_of_lsts)
    create_df_popular_prof_per_year(l_of_lsts, columns)

    # print(d)
    # print(l_of_lsts)
    # print(initiate_popular_prof_of_year_df(d))



    # # data = pd.read_csv('rap_sample_years.csv')
    # # y_1996 = data[data.Date == 1996]
    # # profs_dicts_lst = strings_col_into_dicts_col(y_1996.Profanities, [])
    # # print(profs_dicts_lst)

    # col = create_one_year_dt('rap_sample_years.csv', 1996)
    # profs_dicts_lst = strings_col_into_dicts_col(col, [])
    # print(profs_dicts_lst)
    #
    # # popular_prof_info = find_popular_prof(profs_dicts_lst)
    #
    # # years = create_dt_years_lst('rap_sample_years.csv')
    # # d = find_popular_prof_per_year('rap_sample_years.csv', years)
    # # print(d)


    # l = create_dt_years_lst('rap_sample_years.csv')
    # print(l)
    # print(type(l[0]))
    # # ls = ['1995', '2004', '1990', '2020', '2122', '2018']
    # # print(natsorted(ls))
