# FILE: rap_visualize3.py
# final_project_rap 2021
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


# Themes dict creation
ass = "anal, analanni, analsex, anu, ars, arsehol, ass, assbagg, assblast, assclown, asscowboy, assfuck, asshat, asshol, asshor, assjockey, asskiss, assklown, asslick, asslov, assman, assmonkey, assmunch, asspack, asspir, asspuppi, assrang, asswhor, asswip, butt, buttbang, buttfac, buttfuck, butthead, buttman, buttmunch, buttpir, buttplug, buttstain, buttfac, rimjob, suckmyass, bigass, fatass, dumbass, intheass, jackass, kissass, bigbutt, upthebutt, uptheass, booti, bootycal, rim, bunga, bunghol, cornhol, rearend, rearentri, boodi, glazeddonut, enema, bugger, buggeri"
feecees = "shitfuck, shitdick, bullshit, dipshit, horseshit, jackshit, shhit, shit, shitcan, shite, shiteat, shitfac, shitfit, shitforbrain, shitful, shithapen, shithappen, shithead, shithous, shitlist, shitola, shitoutofluck, shitstain, shitter, shitti, pee, peehol, peepe, piss, pisser, pisshead, pissin, pissoff, poop, pooper, pooperscoop, turd, crap, crapola, crapper, crappi, pi55, barfac, barffac, barf, krap, krappi, goldenshow, doodoo, bullcrap, farti, phuke, tinkle, dingleberri, poo, scat, shat, whiz"
sex = "anal, analanni, analsex, anu, assfuck, backdoorman, buttbang, buttfuck, buttplug, sex, sexfarm, sexhound, sexhous, sexkitten, sexpot, sexslav, sextogo, sextoy, sexwhor, sexi, sexymoma, sexyslim, badfuck, bumblefuck, bumfuck, buttfac, dumbfuck, facefuck, cuntfuck, cuntlick, cuntsuck, fannyfuck, fastfuck, fatfuck, fingerfuck, fistfuck, footfuck, freakfuck, freakyfuck, freefuck, fuc, fucck, fuck, fucka, fuckabl, fuckbag, fuckbuddi, fuckedup, fucker, fuckfac, fuckfest, fuckfreak, fuckfriend, fuckhead, fuckher, fuckin, fuckina, fuckingbitch, fuckinnut, fuckinright, fuckit, fuckknob, fuckm, fuckmehard, fuckmonkey, fuckoff, fuckpig, fucktard, fuckwhor, fuckyou, fuk, funfuck, fuuck, gangbang, gaymuthafuckinwhor, goddamnmuthafuck, barfac, barffac, headfuck, mothafuck, mothafucka, mothafuckaz, mothafuckin, motherfuck, motherfuckin, nofuckingway, nutfuck, pussyfuck, rentafuck, shitfuck, shortfuck, skankfuck, stupidfuck, titfuck, titfuckin, unfuck, whorefuck, blowjob, breastjob, handjob, hosejob, lubejob, rimjob, titjob, dicklick, suckmydick, suckdick, cocklick, cocklov, cocksuc, cocksuck, cockteas, pussyeat, pussylick, pussylov, pussypound, eatpussi, breastlov, titlick, titlov, balllick, intheass, shitfac, bang, doggiestyl, doggystyl, deapthroat, deepthroat, fu, fubar, porn, pornflick, pornk, porno, pornprincess, pimp, pimper, pimpjuic, pimpsimp, popimp, shawtypimp, xxx, triplex, bootycal, brothel, virginbreak, sixtynin, spigotti, footact, footlick, forni, fornic, fckcum, felatio, felch, felcher, fellatio, feltch, feltcher, cuck, givehead, orgi, horney, horniest, horni, noonan, nooner, phuq, fok, mattressprincess, phuk, quicki, ero, threeway, tongethrust, tonguethrust, wetback, wetspot, glazeddonut, enema, inthebuff, gummer, clamdigg, gonorrehea, hottotrot, iblowu, spreadeagle, chickslick, Juggalo, fugli, peepshow, peepshpw, lapdanc, scat, rump, shag, shaggin, slideitin, tuckahoe, mofo, playboy, playgirl, suckm, suckoff, swallow, turnon, snowback, dildo, taff, coitu, clamdiv, bugger, buggeri, crotchjockey, hodgi, licker, Lolita, hustler, wtf, uck, uk, spank"
dick = "dick, dickbrain, dickforbrain, dickhead, dickless, dicklick, dickman, dickwad, dickwe, suckmydick, dripdick, limpdick, shitdick, suckdick, pindick, whiskeydick, whiskydick, cock, cockblock, cockcowboy, cockfight, cockhead, cockknob, cocklick, cocklov, cocknob, cockqueen, cockrid, cocksman, cocksmith, cocksmok, cocksuc, cocksuck, cockteas, hiscock, balllick, ball, ballsack, spermbag, boner, meatsack, kock, dix, dong, lovebon, lovegun, lovemuscl, lovepistol, loverocket, pecker, pud, pudboy, pudd, puddboy, erect, thirdleg, mosshead, manpast, choad, chode, hardon, dipstick, schlong, scrotum, nudger, skinflut, munt, eatbal"
pussy = "pussycat, pussyeat, pussylick, pussylip, pussylov, pussypound, puss, pussi, pusi, eatpussi, hotpussi, clit, cunntt, cunt, cuntfuck, cuntlick, cuntsuck, pu55i, pussyfuck, kunt, camelto, poontang, luckycammelto, nook, nookey, nooki, muff, muffdiv, muffindiv, mufflikc, cherrypopp, crotchrot, flang, poon, queef, fingerfood, puntang, quim, tang, vulva"
breasts = "breastjob, breastlov, breastman, breastjob, tit, titbitnippli, titlick, titlov, titti, nittit, suckmytit, titfuck, titfuckin, titjob, boob, boobi, hooter, bazonga, bazoom, honk, honker, honkey, honki, knocker, gonzaga, teat, jug"
black = "datnigga, nig, niger, Nigerian, nigg, nigga, niggah, niggaracci, niggard, niggardli, niggaz, nigger, niggerhead, niggerhol, niggl, niggor, niggur, niglet, nignog, nigr, nigra, nip, nlgger, nlggor, sandnigg, snigger, snownigg, spaghettinigg, timbernigg, whitenigg, negro, negroid, darki, kaffer, kaffir, kaffr, kafir, picaninni, piccaninni, pickaninni, jigaboo, jiga, jigga, jiggabo, alligatorbait, thicklip, coon, coondog, koon, gatorbait, jijjiboo, mooncricket, junglebunni, porchmonkey, macaca, jimfish, kkk, mulatto, tarbabi, zigabo"
mysogynistic = "bitch, bitcher, bitchez, bitchin, bitchslap, bitchi, dumbbitch, nastybitch, skank, skankbitch, skankwhor, skanki, skankybitch, skankywhor, cuntey, cunt, biatch, crackwhor, nastyho, nastyslut, nastywhor, slut, slutt, slutti, slutwear, slutwhor, whore, whorehous, twobitwhor, easyslut, asswhor, sexwhor, fuckwhor, gaymuthafuckinwhor, whorefuck, sonofabitch, sonofbitch, fuckingbitch, kunt, byatch, milf, hooker, hore, tramp, thot, pornprincess, henhouse, ho, hoe, mattressprincess, hussi, holestuff, ontherag, booni, randi, splittail"
lgbt_phobic = "gay, gaymuthafuckinwhor, fag, faggot, fagot, homo, homobang, tranni, transexu, transsexu, transvestit, sodomis, sodomit, Sodom, sodomi, queer, lesbo, lez, lezb, lezbefriend, lezbo, lezz, lezzo, sissi, twink, twinki, butchbab, butchdik, butchdyk, fudgepack, dyke, bulldik, bulldyk, muncher"
masturbation = "jackoff, meatbeatt, jerkoff, wank, wanker, williewank, mastab, mastabat, masterb, masterblast, mastrab, masturb, beatoff, beatyourmeat, pocketpool, spankthemonkey, smackthemonkey, diddl"
sperm = "cum, cumbubbl, cumfest, cumjockey, cumm, cummer, cumquat, cumqueen, cumshot, cunn, spermacid, spermbag, spermheard, spermherd, jism, jiz, jizim, jizjuic, jizm, jizz, jizzim, jizzum, semen, geez, geezer, jeez, pimpjuic, kum, lovegoo, lovejuic, spunk, spunki, spoog, kummer"
general = "idiot, stupid, sucker, moron, dumb, bastard, bigbastard, dammit, damn, damnit, godammit, goddamit, goddammit, goddamn, goddamnit, mad, tard, bollick, bollock, kumquat, hotdamn, skumbag, sleezebag, sleezebal, jesu, jesuschrist, loser, scallywag, boang, hell, pric, prick, prickhead, Dahmer, gotohel, looser, screwyou, welcher, retard, twat, scum, gipp, rere, skum, whacker, dink, quashi, lowlif"
anti_asian = "chinaman, chinamen, jap, japcrap, yellowman, slant, slantey, paki, hindoo, kotex, slopehead, kigger, honger, zipperhea, phungki, raghead, gook, hapa"
antisemitic = "jew, kike, kyke, goy, goyim, hebe, heeb, jigger, mockey, mocki, cohe"
islamophobic = "cameljockey, carpetmunch, moslem, palesimian, towelhead, raghead"
anti_white = "poorwhitetrash, whitetrash, whitey, hillbilli, redneck, peckerwood, gringo, pohm, pom, pommi, limey, limi, kraut, clogwog, greaseball, trailertrash, dago, dego, wigger, gubba, ginzo, polack, lugan, roundey, russki, seppo, payo, whigger, spaghettibend, whop, wop, whash"
drugs = "reefer, bong, fourtwenti, smack, stringer"
anti_latin = "spic, spick, spig, spik, mgger, mggor, beaner, pocha, pocho, wab"
anti_roma = "gyp, gypo, gypp, gyppi, gyppo"
anti_native = "abbo, abo, boong, boonga, squaw"

# UNITED CATEGORIES
CONNECT = ", "
male_anatomy = dick + CONNECT + sperm
female_anatomy = pussy + CONNECT + breasts
non_black = anti_asian + CONNECT + antisemitic + CONNECT + islamophobic + CONNECT + anti_white + CONNECT + anti_latin + CONNECT + anti_roma + CONNECT + anti_native
sex_united = sex + CONNECT + sperm + CONNECT + masturbation

united_prof_themes_dict = {"Female Anatomy": female_anatomy,
                           "Male Anatomy": male_anatomy,
                           "Ass related": ass,
                           "Feecees related": feecees,
                           "Sex related": sex_united,
                           "Black related": black,
                           "Mysogynistic": mysogynistic,
                           "LGBT": lgbt_phobic,
                           "Drugs related": drugs,
                           "Non-Black Slurs": non_black
                           }

categories_dict = {"ass related": ass,
                   "feecees related": feecees,
                   "sex related": sex,
                   "dick related": dick,
                   "pussy related": pussy,
                   "breasts related": breasts,
                   "black related": black,
                   "mysogynistic": mysogynistic,
                   "LGBT": lgbt_phobic,
                   "masturbation": masturbation,
                   "sperm": sperm,
                   "drugs related": drugs,
                   "anti asian": anti_asian,
                   "antisemitic": antisemitic,
                   "islamophobic": islamophobic,
                   "anti white": anti_white,
                   "anti latin": anti_latin,
                   "anti roma": anti_roma,
                   "anti native": anti_native,
                   }


def get_n_longest_values_g(dictionary, n):
    """
    A function that finds the n longest iterables in a given dictionary.
    :param dictionary: A dictionary in the format of {"key": iterable item}
    :param n: The number of items we wan to have at the end of the run.
    :return: A list of tuples in the format of [("key", a number for the length
     of it's value in the original dictionary)].
    """
    longest_entries = sorted(
        dictionary.items(), key=lambda t: len(t[1]), reverse=True)[:n]
    return [(key, len(value)) for key, value in longest_entries]


def create_valid_themes_dict(dicti):
    """
    A function that converts a dictionary values of strings, into a list of
    words.
    :param dicti: A dictionary in the format of {"key": "word1, word2,..word"}
    :return: A dictionary in the format of {"key": ["word1", "word2", "word"]}
    """
    new_dict = {}
    for key, val in dicti.items():
        new_dict[key] = val.split(", ")
    return new_dict


def create_top_n_themes_dict(dicti, n):
    """
    A function that validates a dictionary key="string" and value=["list", "of"
    , "words"] and than creates a new dictionary of the n longest pairs of that
    dictionary, by their values' length.
    :param dicti: A dictionary in the format of {"key": "word1, word2,..word"}
    :param n: The number of items we wan to have in our new dictionary at the
    end of the run.
    :return: A dictionary of the longest items of the original dictionary, by
    the length of their values.
    """
    valid_dict = create_valid_themes_dict(dicti)
    dict_top_n = get_n_longest_values_g(valid_dict, n)
    valid_top_ten_dict = {}
    for item in dict_top_n:
        key = item[0]
        valid_top_ten_dict[key] = valid_dict[key]
    return valid_top_ten_dict

# END OF PREPARATION


# GROUPS COMPARISONS
def category_option_most_popular_prof(jsons_list, field, category_option):
    """
    Find the most popular profanity for one field option, in multiple jsons
    data.
    For example: find the most popular profanity in songs written by women.
    :param field: e.g. "Gender", "Ethnicity"
    :param jsons_list: a list of songs data json files.
    :param category_option: e.g. ["Male"] or ["French", "English"..] - A list
    of all the words that can represent the group of which we want to analyze.
    :return: A tuple containing a string for the most popular prof of the
    group's artists songs, and a number for the % it tales aut of all the shows
     of profanities in that group's songs. (e.g. "nigga", 19)
    """
    category_option_profs = {}
    option_total_profs_count = 0
    for json in jsons_list:
        songs_data = pd.read_json(json, orient='table')
        for row in songs_data.iterrows():
            # if the song is not in the group (e.g. the gender or ethnicity
            # list)
            if row[1][field] not in category_option:
                continue
            # if there are no profanities in that song
            if not row[1]["Profanities"]:
                continue
            else:
                # add the number of profanities in that song to the total
                # profanities count of the category option.
                option_total_profs_count += sum(row[1]["Profanities"].values())
                song_profs = row[1]["Profanities"]
                for prof in song_profs.keys():
                    if prof in category_option_profs:
                        category_option_profs[prof] += song_profs[prof]
                    else:
                        category_option_profs[prof] = song_profs[prof]
    # change profs count to percentages:
    for prof, count in category_option_profs.items():
        category_option_profs[prof] = (count / option_total_profs_count) * 100
    category_option_profs_list = list(category_option_profs.keys())
    frequencies = list(category_option_profs.values())
    max_value = max(frequencies)
    # to do: what happens if the same frequency is accurate for more than one
    # prof?
    index_of_frequency = frequencies.index(max_value)
    most_popular_prof = category_option_profs_list[index_of_frequency]
    category_option_top_prof, top_prof_count = most_popular_prof, max_value
    return category_option_top_prof, top_prof_count


def most_popular_prof_per_field_group(jsons_list, field, field_options):
    """
    Compare the most popular profanities in different groups of artists, for
    example: men vs women, Europeans vs Americans.
    :param field: the name of the field in which we want to compare
    different groups, e.g. "Gender")
    :param jsons_list: a list of songs data json files.
    :param field_options: dictionary of the groups we want to compare,
    in a format of {"option_name":[]}
    For example: {"european countries":EU, "american countries": AMERICA}
    or {"male":["male"], "females": ["Female"]}
    :return: A dictionary of key=group, value=(top prof, percentage of shows).
    e.g. {"females": ("nigga", 19)}
    """
    field_summary = {}
    for option, option_list in field_options.items():
        option_info = category_option_most_popular_prof(jsons_list, field,
                                                        option_list)
        field_summary[option] = option_info
    return field_summary


def visual_compare_groups_popular_profs(groups_dict, y_lim, x_label, y_label,
                                        title, colors='blue'):
    """
    A function creating a bar plot.
    :param groups_dict: a dictionary in a format of
    {"group_name": ("word", number)
    :param y_lim: The upper value for the Y ax.
    :param x_label: The label for X.
    :param y_label: The label for Y.
    :param title: A title for the graph.
    :param colors: colors for the bars. Can be a single string or a list of
    strings for multiple colors.
    :return: None
    """
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
    """
    A function that finds the frequency of profanities (%) out of all the
    lyrics of one group of rappers's songs.
    :param jsons_list: a list of songs data json files.
    :param field: e.g. "Gender", "Ethnicity"
    :param group_list: e.g. ["Male"] or ["French", "English"..] - A list
    of all the words that can represent the group of which we want to analyze.
    :return: The group's profanities frequency (a float representing %).
    """
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
        # if there are no songs from that group in any json file.
        return
    group_cursing_frequency = (profs_count / total_words_count) * 100
    return group_cursing_frequency


def cursing_frequency_groups_comparison(jsons_list, field, groups_dict):
    """
    A function that finds the fraction that profanities take, out of all the
    lyrics of each group of artists to compare between the groups.
    :param jsons_list: a list of songs data json files.
    :param field: the name of the field in which we want to compare
    different groups, e.g. "Gender")
    :param groups_dict: dictionary of the groups we want to compare,
    in a format of {"option_name":[]}
    For example: {"european countries":EU, "american countries": AMERICA}
    or {"male":["male"], "females": ["Female"]}
    :return: A dictionary that shows the cursing frequency for each group in
    the format of {"group's name": 12}
    """
    field_profs_frequencies = {}  # group: frequency
    for group, group_list in groups_dict.items():
        profs_freq = find_group_cursing_frequency(jsons_list, field,
                                                  group_list)
        if profs_freq:
            field_profs_frequencies[group] = profs_freq
    return field_profs_frequencies


def bar_plot_cursing_frequencies(freqs_dict, y_lim, x_label, y_label, title,
                                 colors="blue"):
    """
    A function creating a bar plot.
    :param freqs_dict: a dictionary in a format of
    {"group_name": cursing frequency (a float)}
    :param y_lim: The upper value for the Y ax.
    :param x_label: The label for X.
    :param y_label: The label for Y.
    :param title: A title for the graph.
    :param colors: colors for the bars. Can be a single string or a list of
    strings for multiple colors.
    :return: None
    """
    groups = [key for key in freqs_dict.keys()]
    y = [val for val in freqs_dict.values()]
    plt.bar(groups, y, color=colors)
    plt.ylim([0, y_lim])
    for i in range(len(groups)):
        plt.text(i, y[i] + 0.1, f"{round(y[i], 1)}%", ha="center",
                 va="bottom", weight="bold")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
    return


# IN-GROUP ANALYSIS AND VISUALISATION
def ingroup_profs_diversion_counts(json_file, profs_categories, category=None, group=None):
    """
    A function that counts the number of shows of profanities from each theme,
    in one group of artist's songs.
    :param json_file: A string that is the name of one json file.
    :param category: The field we want to explore one group of, e.g. "Gender",
    "Ethnicity"
    :param group: A list of all the words that can represent the group of which
    we want to analyze, e.g. ["Male"] or ["French", "English"..].
    :param profs_categories: A dictionary of profanities themes in the format
    of {"theme": ["prof1", "prof2"..]}
    :return: A dictionary of the profanities themes diversion in one group of
    artist's songs {"theme": an int for the number of shows of profanities from
    that theme}
    """
    songs_data = pd.read_json(json_file, orient='table')
    profs_diversion_by_category = {}
    # a loop that covers each song (row = one song's data)
    for row in songs_data.iterrows():
        if category:
            if row[1][category] not in group:
                continue
        if not row[1]["Profanities"]:
            continue
        else:
            # add the number of words in that song to the total words count of
            # the category option.
            song_profs = row[1]["Profanities"]
            for prof in song_profs.keys():
                found = False
                for i in range(len(profs_categories.keys())):
                    category_key = list(profs_categories.keys())[i]
                    category_words = profs_categories[category_key]
                    if prof in category_words:
                        found = True
                        if category_key in profs_diversion_by_category:
                            profs_diversion_by_category[category_key] += \
                                song_profs[prof]
                        else:
                            profs_diversion_by_category[category_key] = \
                                song_profs[prof]
                    elif i == len(profs_categories.keys()) - 1 and not found:
                        if "others" in profs_diversion_by_category:
                            profs_diversion_by_category["others"] += \
                                song_profs[prof]
                        else:
                            profs_diversion_by_category["others"] = \
                                song_profs[prof]
    return profs_diversion_by_category


# graphs 4, 5
def group_profs_diversion_multiple_json(json_files, prof_categories, category=None,
                                        group_name=None, group=None):
    """
    A function that shows the profanities' themes' diversion in one group
    of artists' songs.
    :param group_name: A string for the group of artists.
    :param json_files: A list of json files names (strings)
    :param category: The string representing the field of which we want to
    explore one group. (e.g. "Gender" or "Ethnicity")
    :param group: The group representative names (["Female"] or ["British",
    "French"]
    :param prof_categories: A dictionary of categories shown as
    key=theme name string, value=theme words list.
    :return: a dictionary of the key, value = theme, percentage.
    """
    group_profs_diversion_dict = {}
    for one_json in json_files:
        one_file_diversion = ingroup_profs_diversion_counts(one_json,
                                                            prof_categories,
                                                            category, group)
        for cat, count in one_file_diversion.items():
            if cat in group_profs_diversion_dict:
                group_profs_diversion_dict[cat] += count
            else:
                group_profs_diversion_dict[cat] = count
    total_prof_shows = sum(group_profs_diversion_dict.values())
    for category_name, count in group_profs_diversion_dict.items():
        group_profs_diversion_dict[category_name] = (count / total_prof_shows)\
                                                    * 100
    # sort the dictionary for the pie legend to be ordered from most popular to
    # least.
    sorted_themes_diversion = {key: value for key, value in
                               sorted(group_profs_diversion_dict.items(),
                                      key=lambda kv: kv[1], reverse=True)}
    # pie chart
    plt.style.use("fivethirtyeight")
    categories = list(sorted_themes_diversion.keys())  # profs themes
    fraction = list(sorted_themes_diversion.values())  # theme percentage
    labels = [f'{s:0.1f}% {l}' for l, s in zip(categories, fraction)]
    explode = [0.01 for i in range(len(labels))]
    colors_list = ["#B91D2D", "#F5921D", "#27317E", "#28AAE1", "#B5D4EF",
                   "#006838", "#39B54A", "#F9ED32", "#68499E", "#BA89F9",
                   "#949597"]
    plt.axis("equal")
    plt.pie(fraction, explode=explode, colors=colors_list)

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()

    plt.legend(labels=labels, loc="center")
    if group_name:
        plt.title(f"Profanities Themes Diversion:\n{group_name} Artists",
                  pad=-30)
    else:
        plt.title(f"Profanities Themes Diversion\nAll Times, Genders & "
                  f"Ethnicities",
                  pad=-30)
    plt.show()
    return sorted_themes_diversion


# 6
def theme_fraction_in_group_pie_chart(percentage, group_name, theme_name):
    """
    Initiate a pie chart that shows the fraction of a songs' group that contain
    profanities from one theme.
    :param percentage: The percentages of the songs that contain the theme.
    :param group_name: The name of the group we want to check songs of (string)
    :param theme_name: The name of the theme we want to check the frequency of
     (string).
    :return: None
    """
    plt.style.use("fivethirtyeight")
    colors_list = ["#FF4545", "#71ED3CC7"]
    fraction = [percentage, 100 - percentage]  # profs themes percentage
    labels = [f"contain {theme_name} profanities",
              f"don't contain {theme_name} profanities"]  # profs themes

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()

    plt.title(
        f"How much of the {group_name} artists' songs\ncontain {theme_name} profanities")
    plt.axis("equal")
    plt.pie(fraction, autopct='%1.1f%%', colors=colors_list,
            textprops={'fontsize': 18, 'fontweight': 'bold'}, pctdistance=1.1, labeldistance=1)
    plt.legend(labels=labels, loc='center')
    plt.show()


# 6 total
def theme_frequency_in_group(jsons_list, field, group_name, group_words, theme,
                             theme_profs_list):
    """
    A function that finds how many songs (%) of artists from the same group,
    contain profanities from a single theme. For example, how many (%) European
    artists' songs contain sex related profanities.
    :param jsons_list: A list of json files names (strings)
    :param field: The string representing the field of which we want to
    explore one group. (e.g. "Gender" or "Ethnicity")
    :param group_name: A string for the group we want to analyze within the
    field.
    :param group_words: The group representative names (["Female"] or
    ["British", "French"].
    :param theme: A string for the theme of profanities we want to analyze.
    :param theme_profs_list: The list of profanities that count in tha theme.
    :return: The percentage (float) of songs of the chosen group of artists
    that contain profanities of the chosen theme.
    """
    num_of_songs_with_theme = 0
    group_songs_count = 0
    for json in jsons_list:
        songs_data = pd.read_json(json, orient='table')
        # a loop that covers each song (row = one song's data)
        for row in songs_data.iterrows():
            contains_theme = False
            if row[1][field] not in group_words:
                continue
            if not row[1]["Profanities"]:
                group_songs_count += 1
                continue
            for prof in row[1]["Profanities"].keys():
                if prof in theme_profs_list:
                    num_of_songs_with_theme += 1
                    group_songs_count += 1
                    contains_theme = True
                    break
            if not contains_theme:
                group_songs_count += 1
    percentage_of_songs_containing_theme = (num_of_songs_with_theme /
                                            group_songs_count) * 100
    print(f"Approximately {round(percentage_of_songs_containing_theme, 0)}"
          f"% of {group_name} artists' songs, use {theme} "
          f"profanities.")
    theme_fraction_in_group_pie_chart(percentage_of_songs_containing_theme,
                                      group_name, theme)
    return percentage_of_songs_containing_theme


# YEARS
def most_popular_profanity_in_year(jsons_list):
    """
    A function to find the most used profanity in every year
    :param jsons_list: A list of json files with the songs dataframe
    :return: A dictionary of key=year, value=(top prof, percentage of shows).
    """
    field_summary = {}
    for i in range(1980, 2022):
        option_info = category_option_most_popular_prof(jsons_list, 'Date',
                                                        [i])
        field_summary[i] = option_info
    return field_summary


def profanity_percent_in_year(jsons_list, field=None, field_option=None):
    """
    A function for showing how frequently songs used profanities in their
    vocabulary
    :param jsons_list: A list of json files with the songs dataframe
    :param field: The category on which we want the specification
    :param field_option: A list of groups of whom we want to count
    :return: A dictionary of years and the percent of profanities in their
    lyrics
    """
    year_dict = {}
    for year in range(1980, 2022):
        year_dict[year] = []
    for json in jsons_list:
        df = pd.read_json(json, orient='table')
        if field is not None:
            new_df = pd.DataFrame()
            for opt in field_option:
                opt_df = df.loc[df[field] == opt]
                new_df = pd.concat([new_df, opt_df], axis=0)
            df = new_df
        for year in range(1980, 2022):
            df_year = df.loc[df['Date'] == year]
            if len(df_year) == 0:
                continue
            lyric_num = 0
            profanity_num = 0
            for row in df_year.iterrows():
                lyric_num += len(row[1]['Lyrics'])
                profanity_num += sum(row[1]["Profanities"].values())
            profanity_percent = (profanity_num / lyric_num) * 100
            year_dict[year].append(profanity_percent)
    for year in range(1980, 2022):
        sum_year = sum(year_dict[year])
        data_length = len(year_dict[year])
        if data_length == 0:
            year_dict[year] = 0
            continue
        year_dict[year] = sum_year / data_length
    return year_dict


def get_population_percent(jsons_list, field, field_option):
    """
    A function which shows the rise and fall of the number of rappers from a
    specific background
    :param jsons_list: A list of json files with the songs dataframe
    :param field: The category on which we want the specification
    :param field_option: A list of groups of whom we want to count
    :return: A dictionary of years and the percent of our chosen groups out
    of the whole database
    """
    year_dict = {}
    for year in range(1980, 2022):
        year_dict[year] = []
    for json in jsons_list:
        df = pd.read_json(json, orient='table')
        for year in range(1980, 2022):
            df_year = df.loc[df['Date'] == year]
            all_songs_in_doc_and_year = len(df_year)
            if all_songs_in_doc_and_year == 0:
                continue
            part = 0
            for opt in field_option:
                part += len(df_year.loc[df_year[field] == opt])
            profanity_percent = (part / all_songs_in_doc_and_year) * 100
            year_dict[year].append(profanity_percent)
    for year in range(1980, 2022):
        sum_year = sum(year_dict[year])
        data_length = len(year_dict[year])
        if data_length == 0:
            year_dict[year] = 0
            continue
        year_dict[year] = sum_year / data_length
    return year_dict


def follow_profanity_type(jsons_list, profanities):
    """
    A function for a dictionary which shows the percent of a profanity type
    in any given year from 1980 to 2021
    :param jsons_list: A list of json files with the songs dataframe
    :param profanities: A string of the name of the profanity type
    :return: A dictionary of years and the percent of that profanity type
    among overall profanities
    """
    year_dict = {}
    for year in range(1980, 2022):
        year_dict[year] = []
    profanity_lst = create_valid_themes_dict(categories_dict)[profanities]
    for json in jsons_list:
        df = pd.read_json(json, orient='table')
        for year in range(1980, 2022):
            df_year = df.loc[df['Date'] == year]
            if len(df_year) == 0:
                continue
            percent_lst = []
            for row in df_year.iterrows():
                song_dict = row[1]['Profanities']
                profanities_num = sum(song_dict.values())
                if profanities_num == 0:
                    continue
                prof_count = 0
                for word in song_dict.keys():
                    if word in profanity_lst:
                        prof_count += song_dict[word]
                profanity_percent = (prof_count / profanities_num) * 100
                percent_lst.append(profanity_percent)
            if not percent_lst:
                continue
            year_dict[year].append(sum(percent_lst) / len(percent_lst))
    for year in range(1980, 2022):
        sum_year = sum(year_dict[year])
        data_length = len(year_dict[year])
        if data_length == 0:
            year_dict[year] = 0
            continue
        year_dict[year] = sum_year / data_length
    return year_dict


if __name__ == '__main__':
    all_genders = {"males": ["Male"], "females": ["Female"]}
    profs_themes = create_top_n_themes_dict(categories_dict,
                                            len(categories_dict.keys()))
    united_prof_themes = create_top_n_themes_dict(united_prof_themes_dict,
                                                  len(united_prof_themes_dict.keys()))
    united_top_5_themes = create_top_n_themes_dict(united_prof_themes_dict, 5)
    # GROUPS COMPARISON
    # 13
    # group_profs_diversion_multiple_json(ALL_JSONS, united_prof_themes)

    # 1: Show the top profanity of each gender's rappers and it's frequency
    # (percentages)
    # genders_top_profs = most_popular_prof_per_field_group(FULL_JSONS, GEN, all_genders)
    # print(genders_top_profs)
    # visual_compare_groups_popular_profs(genders_top_profs, 50,
    #                                      "Rappers' Genders",
    #                                      "Top profanity's frequency (%)",
    #                                      "Most popular profanity - Genders "
    #                                      "Comparison", ["#59AFFF", "#FF85F3"])

    # 2: Most popular prof - geographically
    # geo_groups_top_profs = most_popular_prof_per_field_group(FULL_JSONS, ETHN,
    #                                                          GEO_GROUPS)
    # print(geo_groups_top_profs)
    # visual_compare_groups_popular_profs(geo_groups_top_profs, 50,
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
    #                                                    GEO_GROUPS)
    # print(groups_freqs)
    # bar_plot_cursing_frequencies(groups_freqs, 10, "Rappers' Ethnicity",
    #                              "Profanities fraction of all songs' "
    #                              "lyrics (%)", "Rap Cursing Frequencies - "
    #                                            "Ethnicity Comparison",
    #                              colors=["#F9AF40", "#EC6A0C", "#C11D1D",
    #                                      "#FFF505", "#C11D1D", "#EC6A0C",
    #                                      "#EC6A0C"])

    # IN GROUP GRAPHS

    # 4: Females themes diversion
    # females = all_genders['females']
    # females_diversion = group_profs_diversion_multiple_json(FULL_JSONS,
    #                                                         united_prof_themes,
    #                                                         GEN,
    #                                                         "Female", females)
    # print(females_diversion)
    # bar_plot_cursing_frequencies(females_diversion, 100, "Themes", "Theme's
    # frequency (%)", "Profanities Themes Diversion - Female Artists")

    # 5: Males themes diversion
    males = all_genders['males']
    males_diversion = group_profs_diversion_multiple_json(FULL_JSONS,
                                                          united_prof_themes, GEN,
                                                          "Male", males)
    print(males_diversion)

    # 6: How many songs of a group contain profs from category X?
    theme6 = "black related"
    theme6_profs = profs_themes[theme6]
    per = theme_frequency_in_group(FULL_JSONS, ETHN, "Black", BLACK, theme6,
                                   theme6_profs)


    # 7: Groups of swearwords over the years
    # black_profs = follow_profanity_type(ALL_JSONS, "black related")
    # mysog_profs = follow_profanity_type(ALL_JSONS, "mysogynistic")
    # sex_profs = follow_profanity_type(ALL_JSONS, "sex related")
    # female_body_profs = follow_profanity_type(ALL_JSONS, "pussy_and_breasts")
    # male_body_profs = follow_profanity_type(ALL_JSONS, "dick_and_sperm")
    # plt.title('Profanity Types Over Time')
    # plt.plot(black_profs.keys(),
    #          black_profs.values(), label='Black related')
    # plt.plot(mysog_profs.keys(),
    #          mysog_profs.values(), label='Misogyny related')
    # plt.plot(sex_profs.keys(),
    #          sex_profs.values(), label='Sex related')
    # plt.plot(female_body_profs.keys(),
    #         female_body_profs.values(), label='Female body related')
    # plt.plot(male_body_profs.keys(),
    #         male_body_profs.values(), label='Male body related')
    # plt.legend()
    # plt.xlabel('Year')
    # plt.ylabel('Percentages of Profanities\' Types')
    # plt.legend()
    # plt.show()

    # 8: Percent of Profanities in year
    # profanities_year_percents = profanity_percent_in_year(ALL_JSONS)
    # plt.title('Profanities frequencies over time')
    # plt.plot(profanities_year_percents.keys(),
    # profanities_year_percents.values())
    # plt.xlabel('Year')
    # plt.ylabel('Percentage of Profanities in Rap Songs')
    # plt.show()

    # # 9: How many rappers were from different ethnicities and genders
    # # male_percent_dict = get_population_percent(FULL_JSONS, GEN, ['Male'])
    # # female_percent_dict = get_population_percent(FULL_JSONS, GEN, ['Female'])
    # us_percent_dict = get_population_percent(FULL_JSONS, ETHN, USA)
    # black_percent_dict = get_population_percent(FULL_JSONS, ETHN, BLACK)
    # # europe_percent_dict = get_population_percent(FULL_JSONS, ETHN, EU)
    # # america_percent_dict = get_population_percent(FULL_JSONS, ETHN, AMERICAS)
    # plt.title('Rise of Rappers by Percentage')
    # # plt.plot(male_percent_dict.keys(),
    # #         male_percent_dict.values(), label='Male')
    # # plt.plot(female_percent_dict.keys(),
    # #         female_percent_dict.values(), label='Female')
    # plt.plot(us_percent_dict.keys(),
    #          us_percent_dict.values(), label='USA')
    # plt.plot(black_percent_dict.keys(),
    #          black_percent_dict.values(), label='Blacks')
    # # plt.plot(europe_percent_dict.keys(),
    # #         europe_percent_dict.values(), label='Europe')
    # # plt.plot(america_percent_dict.keys(),
    # #         america_percent_dict.values(), label='America (not US)')
    # plt.legend()
    # plt.xlabel('Year')
    # plt.ylabel('Percentage out of all identified artists')
    # plt.legend()
    # plt.show()
    #
    # # 10: Most popular profanity in every year
    # # year_profanities = (most_popular_profanity_in_year(ALL_JSONS))
    # # visual_compare_groups_popular_profs(year_profanities, 50,
    # #                                    "Most Popular Profanities Evey Year",
    # #                                    "Top profanity's frequency (%)",
    # #                                    "Most popular profanity - Years "
    # #                                    "Comparison")
    #
    # # 11: Percent of Profanities in year according to population
    # male_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    #                                                            GEN, ['Male'])
    # female_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    #                                                              GEN,
    #                                                              ['Female'])
    # plt.title('Percentage of Profanities in Rap Songs According to Gender')
    # plt.plot(male_profanities_year_percents.keys(),
    #          male_profanities_year_percents.values(), label='Male')
    # plt.plot(female_profanities_year_percents.keys(),
    #          female_profanities_year_percents.values(), label='Female')
    # plt.legend()
    # plt.xlabel('Year')
    # plt.ylabel('Percentage of Profanities')
    # plt.legend()
    # plt.show()
    #
    # # 12: Percent of Profanities in year according to population
    # europe_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    #                                                              ETHN, EU)
    # # african_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    # #                                                             ETHN, AF)
    # usa_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    #                                                           ETHN, USA)
    # asian_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    #                                                          ETHN, ASIA)
    # mideast_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    #                                                              ETHN,
    #                                                              MIDDLE_EAST)
    # america_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    #                                                               ETHN,
    #                                                               AMERICAS)
    # # aussi_profanities_year_percents = profanity_percent_in_year(FULL_JSONS,
    # #                                                              ETHN, AUS)
    # plt.title('Profanities Frequencies Over Time According to Ethnicity')
    # plt.plot(europe_profanities_year_percents.keys(),
    #          europe_profanities_year_percents.values(), label='European')
    # # plt.plot(african_profanities_year_percents.keys(),
    # #        african_profanities_year_percents.values(), label='African')
    # plt.plot(usa_profanities_year_percents.keys(),
    #          usa_profanities_year_percents.values(), label='From US')
    # plt.plot(asian_profanities_year_percents.keys(),
    #         asian_profanities_year_percents.values(), label='Asian')
    # plt.plot(mideast_profanities_year_percents.keys(),
    #         mideast_profanities_year_percents.values(),
    #         label='Middle-Eastern')
    # plt.plot(america_profanities_year_percents.keys(),
    #          america_profanities_year_percents.values(), label='America (not '
    #                                                            'US)')
    # plt.plot(aussi_profanities_year_percents.keys(),
    #         aussi_profanities_year_percents.values(), label='Australian')
    # plt.legend()
    # plt.xlabel('Year')
    # plt.ylabel('Percentage of Profanities')
    # plt.legend()
    # plt.show()
