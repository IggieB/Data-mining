import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from wordcloud import WordCloud


FULL_DB_FILES = ["songs_dt_part_" + str(i) + ".json" for i in range(1, 73)]
ARTISTS_DB_FILES = ["songs_dt_w_gen_ethn_part_" + str(i) + ".json" for i in
                    range(1, 31)]
COLUMNS = ["Song", "Artist", "Gender", "Ethnicity", "Album", "Date", "URL",
           "Profanities", "Lyrics"]


def load_json_data(json_files):
    """
    this function takes a list of json files and converts them into one
    dataframe
    :param json_files: The DB json files
    :return: a dataframe
    """
    full_data = pd.DataFrame()
    for file in json_files:
        single_file_df = pd.read_json(file, orient='table')
        full_data = full_data.append(single_file_df)
    return full_data


def unite_lyrics(data_df):
    """
    this function gets a dataframe converts the lyrics column (was scraped
    as a list of strings) into one long string for the clustering
    :param data_df: the data dataframe
    :return: a new dataframe with the same data but the lyrics are a one
    long string
    """
    united_lyrics_df = pd.DataFrame()
    for index, row in data_df.iterrows():
        song_details = [row['Song'], row['Artist'], row['Gender'],
                        row['Ethnicity'], row['Album'], row['Date'],
                        row['URL'], row['Profanities'],
                        " ".join(row['Lyrics'])]
        united_lyrics_df = united_lyrics_df.append(pd.DataFrame(columns=COLUMNS,
                                                  data=[song_details]))
    return united_lyrics_df


def vectorize(vector_target):
    """
    this function vectorizes textual data using TF-IDF Vectorizer
    :param vector_target: the textual data
    :return: the data vectorized
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer.fit_transform(vector_target)


def elbow_method_find_k(elbow_data):
    """
    this function generates an elbow method graph to determine the number of
    clusters preferable for the current data sample.
    :param elbow_data: the vectorized data
    :return: nothing, generates a visual graph
    """
    Sum_of_squared_distances = []
    K = range(2, 10)
    for k in K:
        km = KMeans(n_clusters=k, max_iter=200, n_init=10)
        km = km.fit(elbow_data)
        Sum_of_squared_distances.append(km.inertia_)
    # creating the visual graph
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method')
    plt.show()


def clusters_wordclouds(clusters_labels, clustered_data, clusters_df, true_k):
    """
    this function creates a wordcloud for each cluster and prints the song
    titles included in each cluster
    :param clusters_labels: each cluster's labels from the clustering process
    :param clustered_data: the songs lyrics
    :param clusters_df: the dataframe containing the clustering data (song
    title, vector and cluster)
    :param true_k: the chosen k number
    :return: nothing, generates a visual wordcloud for each cluster.
    """
    result = {'cluster': clusters_labels, 'songs': clustered_data}
    result = pd.DataFrame(result)
    for k in range(0, true_k):
        # preparing the wordcloud data
        s = result[result.cluster == k]
        text = s['songs'].str.cat(sep=' ')
        text = text.lower()
        text = ' '.join([word for word in text.split()])
        # creating the wordcloud
        wordcloud = WordCloud(max_font_size=50, max_words=30,
                              background_color="white").generate(text)
        # printing the song titles in each cluster
        print('Cluster: {}'.format(k))
        print('Titles')
        titles = clusters_df[clusters_df.cluster == k]['title']
        print(titles.to_string(index=False))
        # visualizing the wordcloud
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()


def cluster_by_lyrics(cluster_data_titles, k_num, vectorized_data):
    """
    this function executes the actual clustering by using sklearn's KMeans.
    :param cluster_data_titles: the songs titles
    :param k_num: the number of clusters chosen
    :param vectorized_data: the songs lyrics after vectorizing.
    :return: the clusters labels, a new dataframe with data relevant to the
    clustering process and the kmeans model.
    """
    model = KMeans(n_clusters=k_num, init='k-means++', max_iter=500,
                   n_init=20)
    model.fit(vectorized_data)
    labels = model.labels_
    clusters_df = pd.DataFrame(list(zip(cluster_data_titles, labels, vectorized_data)),
                           columns=['title', 'cluster', 'vector'])
    print(clusters_df)
    return labels, clusters_df, model


def visualize_clusters(clusters_df):
    """
    this function creates a scatter plot for the previously created clusters.
    :param clusters_df: the dataframe generated in the clustering process
    :return: nothing, generates a scatter plot.
    """
    # creating x and y coordinates
    pca = PCA(n_components=2)
    two_dim = pca.fit_transform(X.todense())
    x_coordinates = []
    y_coordinates = []
    for coord in two_dim:
        x_coordinates.append(float(coord[0]))
        y_coordinates.append(float(coord[1]))
    # creating color pool for the graph clusters
    colors = ['#AE2424', '#8C448D', '#BDABDF', '#1976D3', '#4FC2F8',
              '#215934', '#A4C447', '#FEC107', '#FF7000', '#815018']
    clusters_df['c'] = clusters_df.cluster.map(
        {0: colors[0], 1: colors[1], 2: colors[2], 3: colors[3], 4: colors[4],
         5: colors[5], 6: colors[6], 7: colors[7], 8: colors[8], 9: colors[9]})
    # creating the scatter plot
    plt.scatter(x_coordinates, y_coordinates, c=clusters_df.c, alpha=0.9, s=10)
    legend_elements = [Line2D([0], [0], marker='o', color='w',
                              label='Cluster {}'.format(i + 1),
                              markerfacecolor=mcolor, markersize=5) for
                       i, mcolor in enumerate(colors[:true_k])]
    plt.title('Clustering by songs lyrics\n', loc='left', fontsize=22)
    plt.legend(handles=legend_elements, loc='upper right')
    plt.show()

if __name__ == '__main__':
    ############ Loading the data ##########3
    full_data_df = load_json_data(ARTISTS_DB_FILES)
    # warning!!!!! the clustering process becomes more accurate the bigger
    # the sample is. That being said it also takes longer:
    # n = 1000 ~ 2 minutes
    # n = 3000 ~ 4 minutes
    # n = 5000 ~ 7 minutes
    # and so on...
    full_data_df_frac = unite_lyrics(full_data_df.sample(n = 3000))
    songs_lyrics = full_data_df_frac["Lyrics"]
    songs_titles = full_data_df_frac["Song"]
    ############ Vectorizing ##################
    X = vectorize(songs_lyrics)
    ############ Elbow Method ##################
    elbow_method_find_k(X)
    ############### Clustering ###############
    true_k = int(input("Please choose a number of cluster: "))
    labels, clusters_df, kmeans = cluster_by_lyrics(songs_titles, true_k, X)
    ################# word clouds #####################
    clusters_wordclouds(labels, songs_lyrics, clusters_df[['title',
                                                           'cluster']], true_k)
    ############ Visualize clusters ############
    visualize_clusters(clusters_df)
