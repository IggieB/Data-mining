# FILE: rap_visualize2.py.py
# WRITER:lee matan,leem72,207378803
# EXERCISE:intro2cse rap_Lee 2020
# DESCRIPTION:
# NOTES:


import pandas as pd
from matplotlib import pyplot as plt
import json
from natsort import natsorted

FAG = ('FAG', ['fag', 'fagging', 'faggot', 'fagot', 'fairy'])
PUSS = ('PUSS', ['puss', 'pussie', 'pussies', 'pussy', 'pussycat', 'pussyeater',
         'pussyfucker', 'pussylicker', 'pussylips', 'pussylover',
         'pussypounder', 'pusy'])
NIG = ('NIG', ['niggard', 'nigga', 'niggaz', 'nigger', 'niggers', 'niggle', 'niggles', 'niggor',
       'niggur', 'nigr'])


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


def num_performances_of_prof_category_a_year(y_dt, profs_category_lst):
    total_category_shows = 0
    year_profs_all_dicts = strings_col_into_dicts_col(y_dt.Profanities, [])
    for dic in year_profs_all_dicts:
        for prof in profs_category_lst:
            if prof in dic:
                total_category_shows += dic[prof]
    return total_category_shows


def categories_frequency_over_time(dt):
    years = create_dt_years_lst(dt)
    categories = [PUSS, NIG, FAG]
    frequencies_dict = {PUSS[0]: {}, NIG[0]: {}, FAG[0]: {}}
    for category in categories:
        for year in years:
            data = create_one_year_dt(dt, year)
            total = num_performances_of_prof_category_a_year(data, category[1])
            frequencies_dict[category[0]][year] = total
    return frequencies_dict


def create_one_category_frequ_df_over_time(dic, category):
    d = {}
    x = list(dic[category].keys())
    y = list(dic[category].values())
    d['Year'] = x
    d['Frequency'] = y
    df = pd.DataFrame(d, columns=['Year', 'Frequency'])
    return df


if __name__ == '__main__':
    # d = categories_frequency_over_time('rap_sample_years.csv') - this file
    # does not exist anymore!!!
    # print(d)
    puss_df = create_one_category_frequ_df_over_time(d, PUSS[0])
    nig_df = create_one_category_frequ_df_over_time(d, NIG[0])
    fag_df = create_one_category_frequ_df_over_time(d, FAG[0])
    plt.title('Profanities categories frequencies over time')

    plt.plot(puss_df.Year, puss_df.Frequency, label='Pussy related')
    plt.plot(nig_df.Year, nig_df.Frequency, label='Nigga related')
    plt.plot(fag_df.Year, fag_df.Frequency, label='Faggot related')

    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Total Performances in Rap Songs')
    plt.legend()
    plt.show()


