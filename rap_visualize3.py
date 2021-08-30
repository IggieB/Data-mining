# FILE: rap_visualize3.py
# WRITER:lee matan,leem72,207378803
# final_project_rap 2020
# DESCRIPTION:
# NOTES:

import pandas as pd
import matplotlib.pyplot as plt

GEN, ETHN = "Gender", "Ethnicity"
FULL_JSONS = ["songs_dt_w_gen_ethn_part_{}.json".format(i) for i in
              range(1, 31)]
ALL_JSONS = ["songs_dt_part_{}.json".format(i) for i in
              range(1, 73)]
EN_SPEAKER = []

EU = ["French", "Spanish", "English", "German", "British", "Black British"]
AF = ["South African", "Nigerian"]
USA = ["Native American", "African-American", "American-Caribbean",
       "American-Haitian", "American-Jamaican", "American-Hispanic and Latino",
       "American-Panamanian", "American-Dominican Republic",
       "American-Mexican",
       "American-Asian", "American-East Asian", "American-Filipino",
       "Puerto Rican"]
ASIA = ["South Korean"]
MIDDLE_EAST = ["Palestinian", "Moroccan"]
AMERICAS = ["Mexican", "Canadian"]
AUS = ["Australian"]

GEO_GROUPS = {"Europeans": EU, "Africans": AF, "USA": USA, "Asians": ASIA,
              "Middle Eastern": MIDDLE_EAST,
              "Americans\n(outside the USA)": AMERICAS, "Australians": AUS}

BLACK = ["Black British", "South African", "Nigerian", "African-American",
         "American-Jamaican"]

PROFS_THEMES = {"pussy related": ["eatpussi", "hotpussi", "puss", "pussi",
                                  "pussycat", "pussyeat", "pussyfuck",
                                  "pussylick", "pussylip", "pussylov",
                                  "pussypound", "pusi"],
                "Nigga related": ["nigga", "niggas"],
                "Cock related": ["cock", "cockblock", "cockcowboy",
                                 "cockfight", "cockhead", "cockknob",
                                 "cocklick", "cocklov", "cocknob",
                                 "cockqueen", "cockrid", "cocksman",
                                 "cocksmith", "cocksmok", "cocksuc",
                                 "cocksuck", "cockteas"]}


# may be deleted at the end
def song_prof_fraction(prof_dict, lyrics):
    total_words_count = len(lyrics)
    profs_count = sum(prof_dict.values())
    profs_fraction = (profs_count / total_words_count) * 100
    return profs_fraction


# groups comparison
def category_option_most_popular_prof(jsons_list, field, category_option):
    """
    Find the most popular profanity for one field option, in multiple jsons
    data.
    For example: find the most popular profanity in songs written by women.
    :param field: e.g. "Gender", "Ethnicity"
    :param jsons_list: a list of songs data json files.
    :param category_option: e.g. ["Male"] or ["French", "English"..]
    :return: A tuple containing a string for the most popular prof of the
    group's artists songs, and a number for how many times it shows in that
    group's songs. (e.g. "nigga", 513)
    """
    category_option_profs = {}
    option_total_profs_count = 0
    for json in jsons_list:
        songs_data = pd.read_json(json, orient='table')
        for row in songs_data.iterrows():
            # if the song is not in the group (e.g. the gender or ethnicity list)
            if row[1][field] not in category_option:
                continue
            # if there are no profanities in that song
            if not row[1]["Profanities"]:
                # add the number of words in that song to the total words count of
                # the category option.
                option_total_profs_count += sum(row[1]["Profanities"].values())
                continue
            else:
                # add the number of words in that song to the total words count of
                # the category option.
                option_total_profs_count += sum(row[1]["Profanities"].values())
                song_profs = row[1]["Profanities"]
                for prof in song_profs.keys():
                    if prof in category_option_profs:
                        category_option_profs[prof] += song_profs[prof]
                    else:
                        category_option_profs[prof] = song_profs[prof]
    # change profs frequencies to percentages:
    # delete the for loop below for count only
    for prof, count in category_option_profs.items():
        category_option_profs[prof] = (count / option_total_profs_count) * 100
    category_option_profs_list = list(category_option_profs.keys())
    frequencies = list(category_option_profs.values())
    max_value = max(frequencies)
    # to do: what happens if the same frequency is accurate for more than one prof?
    index_of_frequency = frequencies.index(max_value)
    most_popular_prof = category_option_profs_list[index_of_frequency]
    category_option_top_prof, top_prof_count = most_popular_prof, max_value
    return category_option_top_prof, top_prof_count


def most_popular_prof_per_field_group(jsons_list, field, field_options):
    """
    Compare the most popular profanities in different groups of artists, for
    example: men vs women, Europeans vs Americans.
    :param field: the name of the field of which we want to compare
    different groups, e.g. "Gender")
    :param jsons_list: a list of songs data json files.
    :param field_options: dictionary of the groups we want to compare, where
    in a format of {"option":[]}.
    For example: {"european countries":EU, "american countries": AMERICA}
    or {"male":["male"], "females": ["Female"]}
    :return: A dictionary of key=group, value=(top prof, percentage of shows).
    """
    field_summary = {}
    for option, option_list in field_options.items():
        option_info = category_option_most_popular_prof(jsons_list, field,
                                                        option_list)
        field_summary[option] = option_info
    return field_summary


def visual_compare_groups_popular_profs(groups_dict, y_lim, x_label, y_label,
                                        title, colors='blue'):
    groups = groups_dict.keys()
    profs = [val[0] for key, val in groups_dict.items()]
    y = [val[1] for key, val in groups_dict.items()]
    plt.bar(groups, y, color=colors)
    plt.ylim([0, y_lim])
    for i in range(len(groups)):
        plt.text(i, y[i] + 2, f"{profs[i]}\n{round(y[i], 1)}%", ha="center",
                 va="bottom", weight="bold")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
    return


def find_group_cursing_frequency(jsons_list, field, group_list):
    total_words_count = 0
    profs_count = 0
    for json in jsons_list:
        songs_data = pd.read_json(json, orient='table')
        for row in songs_data.iterrows():
            if row[1][field] in group_list:
                if row[1]["Profanities"]:
                    song_profs_count = sum(row[1]["Profanities"].values())
                    profs_count += song_profs_count
                total_words_count += len(row[1]["Lyrics"])
    if not total_words_count:
        return
    group_cursing_frequency = (profs_count / total_words_count) * 100
    return group_cursing_frequency


def cursing_frequency_groups_comparison(jsons_list, field, groups_dict):
    field_profs_frequencies = {}  # group: frequency
    for group, group_list in groups_dict.items():
        profs_freq = find_group_cursing_frequency(jsons_list, field,
                                                  group_list)
        if profs_freq:
            field_profs_frequencies[group] = profs_freq
    return field_profs_frequencies


def bar_plot_cursing_frequencies(freqs_dict):
    x = [key for key in freqs_dict.keys()]
    y = [val for val in freqs_dict.values()]
    plt.bar(x, y)
    plt.show()
    return


# inside group visualization


def ingroup_profs_diversion(json_file, category, group, profs_categories):
    """
    :param json_file:
    :param category: Gender, Ethnicity
    :param group: list of group words ["Male"] or ["British", "French"]
    :param profs_categories:
    :return:
    """
    songs_data = pd.read_json(json_file, orient='table')
    profs_diversion_by_category = {}
    total_number_of_songs = 0
    # a loop that covers each song (row = one song's data)
    for row in songs_data.iterrows():
        if row[1][category] not in group:
            continue
        if not row[1]["Profanities"]:
            total_number_of_songs += 1
            continue
        else:
            # add the number of words in that song to the total words count of
            # the category option.
            total_number_of_songs += 1
            song_profs = row[1]["Profanities"]
            for prof in song_profs.keys():
                for i in range(len(profs_categories.keys())):
                    category_key = list(profs_categories.keys())[i]
                    category_words = profs_categories[category_key]
                    if prof in category_words:
                        if category_key in profs_diversion_by_category:
                            profs_diversion_by_category[category_key] += \
                                song_profs[prof]
                        else:
                            profs_diversion_by_category[category_key] = \
                                song_profs[prof]
                    elif i == len(profs_categories.keys()) - 1:
                        if "others" in profs_diversion_by_category:
                            profs_diversion_by_category["others"] += \
                                song_profs[prof]
                        else:
                            profs_diversion_by_category["others"] = \
                                song_profs[prof]
        # change profs frequencies to percentages
        # delete the for loop below for count only
    # total_prof_shows = sum(profs_diversion_by_category.values())
    # for category_name, count in profs_diversion_by_category.items():
    #     profs_diversion_by_category[category_name] = (count / total_prof_shows) * 100
    return profs_diversion_by_category


def group_profs_diversion_multiple_json(json_files, category, group,
                                        prof_categories):
    """
    A function that shows the themes of profanities the perform on songs
    written by one group of artists, and how they diverse.
    :param json_files: A list of json files names (strings)
    :param category: The string representing the field of which we want to
    explore one group. (e.g. "Gender" or "Ethnicity")
    :param group: the group representative names (["Female"] or ["British", "French"]
    :param prof_categories: A dictionary of categories shown as
    key(category name string), value(category words list)
    :return: a dictionary of the key, value = category, percentage.
    """
    group_profs_diversion_dict = {}
    for one_json in json_files:
        one_file_diversion = ingroup_profs_diversion(one_json, category, group,
                                                     prof_categories)
        for cat in one_file_diversion.keys():
            if cat in group_profs_diversion_dict:
                group_profs_diversion_dict[cat] += one_file_diversion[cat]
            else:
                group_profs_diversion_dict[cat] = one_file_diversion[cat]
    total_prof_shows = sum(group_profs_diversion_dict.values())
    for category_name, count in group_profs_diversion_dict.items():
        group_profs_diversion_dict[category_name] = (
                                                            count / total_prof_shows) * 100
    return group_profs_diversion_dict


def diversion_pie_chart(dictionary):
    categories = list(dictionary.keys())
    fraction = list(dictionary.values())
    plt.axis("equal")
    plt.pie(fraction, labels=categories, autopct="%1.2f%%", shadow=True)
    plt.show()


def most_popular_profanity_in_year(jsons_list):
    field_summary = {}
    for i in range(1980, 2022):
        option_info = category_option_most_popular_prof(jsons_list, 'Date', [i])
        field_summary[i] = option_info
    return field_summary


def update_year_dict(dataframe, year_dict):
    for year in range(1980, 2022):
        df_year = dataframe.loc[dataframe['Date'] == year]
        if len(df_year) == 0:
            continue
        lyric_num = 0
        profanity_num = 0
        for row in df_year.iterrows():
            lyric_num += len(row[1]['Lyrics'])
            profanity_num += sum(row[1]["Profanities"].values())
        profanity_percent = (profanity_num / lyric_num) * 100
        year_dict[year].append(profanity_percent)
    return(year_dict)


def profanity_percent_in_year(jsons_list, field=None, field_options=None):
    if field is None:
        year_dict = {}
        for year in range(1980, 2022):
            year_dict[year] = []
        for json in jsons_list:
            df = pd.read_json(json, orient='table')
            year_dict = update_year_dict(df, year_dict)
        for year in range(1980, 2022):
            year_dict[year] = sum(year_dict[year]) / len(year_dict[year])
        return [year_dict]
    else:
        for options in field_options.items():
            print(1)


if __name__ == '__main__':
    all_genders = {"males": ["Male"], "females": ["Female"]}
    # GROUPS COMPARISON

    # 1: Show the top profanity of each gender's rappers and it's frequency
    # (percentages)
    # genders_top_profs = most_popular_prof_per_field_group(FULL_JSONS, GEN, all_genders)
    # print(genders_top_profs)
    # visual_compare_groups_popular_profs(genders_top_profs, 50,
    #                                     "Rappers' Genders",
    #                                     "Top profanity's frequency (%)",
    #                                     "Most popular profanity - Genders "
    #                                     "Comparison", ["#59AFFF", "#FF85F3"])

    # 2: Most popular prof - geographically
    # geo_groups_top_profs = most_popular_prof_per_field_group(FULL_JSONS, ETHN,
    #                                                          GEO_GROUPS)
    # print(geo_groups_top_profs)
    # visual_compare_groups_popular_profs(geo_groups_top_profs, 70,
    #                                     "Rappers' Ethnicity",
    #                                     "Top profanity's frequency (%)",
    #                                     "Most popular profanity - "
    #                                     "Ethnicity Comparison", ["#7D708E",
    #                                                              "#BA89F9",
    #                                                              "#BA89F9",
    #                                                              "#7437C1",
    #                                                              "#BA89F9",
    #                                                              "#BA89F9",
    #                                                              "#340275"])

    # 3: How frequently each geographical group's rappers curse?
    # groups_freqs = cursing_frequency_groups_comparison(FULL_JSONS, ETHN,
    # GEO_GROUPS) print(groups_freqs) bar_plot_cursing_frequencies(
    # groups_freqs)

    # IN GROUP GRAPHS

    # 4: Females themes diversion
    # females = all_genders['females']
    # females_diversion = group_profs_diversion_multiple_json(FULL_JSONS, GEN,
    #                                                         females,
    #                                                         PROFS_THEMES)
    # print(females_diversion)
    # diversion_pie_chart(females_diversion)

    # 5: Males themes diversion
    # males = all_genders['males']
    # males_diversion = group_profs_diversion_multiple_json(FULL_JSONS, GEN,
    #                                                       males,
    #                                                       PROFS_THEMES)
    # print(females_diversion)
    # diversion_pie_chart(females_diversion)
    # 6: Most popular profanity in every year
    # year_profanities = (most_popular_profanity_in_year(ALL_JSONS))
    year_profanities = {1980: ('nigga', 28.26086956521739), 1981: ('nigga', 23.703703703703706), 1982: ('nigga', 30.69544364508393), 1983: ('shit', 34.95145631067961), 1984: ('sucker', 19.34156378600823), 1985: ('nigga', 20.709491850431448), 1986: ('nigga', 13.432835820895523), 1987: ('nigga', 13.040901007705989), 1988: ('fuck', 13.253279964420726), 1989: ('fuck', 9.451130026416202), 1990: ('shit', 10.114444788122487), 1991: ('fuck', 12.25094238018309), 1992: ('nigga', 11.832448236768304), 1993: ('nigga', 15.104812200247885), 1994: ('nigga', 18.8470172422028), 1995: ('nigga', 22.074542243702947), 1996: ('nigga', 20.056889370492026), 1997: ('nigga', 22.376703327107975), 1998: ('nigga', 25.90283517194294), 1999: ('nigga', 25.55496100274035), 2000: ('nigga', 23.48213921485974), 2001: ('nigga', 21.230448383733055), 2002: ('nigga', 21.041923551171394), 2003: ('nigga', 18.64816656947827), 2004: ('nigga', 16.710428625753764), 2005: ('nigga', 19.29318974670105), 2006: ('nigga', 18.7636270360395), 2007: ('nigga', 23.12925170068027), 2008: ('nigga', 22.160737812911727), 2009: ('nigga', 20.118555190046575), 2010: ('nigga', 18.00212183818192), 2011: ('nigga', 19.725118749824336), 2012: ('nigga', 20.619781103254216), 2013: ('nigga', 26.873959775389256), 2014: ('nigga', 26.52451336725628), 2015: ('nigga', 27.280658025922232), 2016: ('nigga', 26.15596033627937), 2017: ('nigga', 21.80208275324386), 2018: ('nigga', 22.941344369915797), 2019: ('nigga', 24.880778911114053), 2020: ('nigga', 22.831050228310502), 2021: ('nigga', 26.508425439391193)}
    visual_compare_groups_popular_profs(year_profanities, 50,
                                        "Most Popular Profanities Evey Year",
                                        "Top profanity's frequency (%)",
                                        "Most popular profanity - Years "
                                        "Comparison")
    # 7: Percent of Profanities in year
    profanities_year_percents = profanity_percent_in_year(FULL_JSONS)
    plt.title('Profanities frequencies over time')

    plt.plot(profanities_year_percents.keys(), profanities_year_percents.values())

    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Percentage of Profanities in Rap Songs')
    plt.legend()
    plt.show()
