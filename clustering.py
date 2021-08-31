import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score
from wordcloud import WordCloud


TEST_FILE = ["clustering_test_file.json"]
DATA_FILES = ["songs_dt_part_" + str(i) + ".json" for i in range(1, 73)]
ARTISTS_FILES = ["songs_dt_w_gen_ethn_part_" + str(i) + ".json" for i in
                 range(1, 31)]
COLUMNS = ["Song", "Artist", "Gender", "Ethnicity", "Album", "Date", "URL",
           "Profanities", "Lyrics"]


def load_json_data(json_files):
    full_data = pd.DataFrame()
    for file in json_files:
        single_file_df = pd.read_json(file, orient='table')
        full_data = full_data.append(single_file_df)
    return full_data


def unite_lyrics(data_df):
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
    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer.fit_transform(vector_target)


def elbow_method_find_k(elbow_data):
    Sum_of_squared_distances = []
    K = range(2, 10)
    for k in K:
        km = KMeans(n_clusters=k, max_iter=200, n_init=10)
        km = km.fit(elbow_data)
        Sum_of_squared_distances.append(km.inertia_)
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method')
    plt.show()


def clusters_wordclouds(clusters_labels, clustered_data, clusters_df, true_k):
    result = {'cluster': clusters_labels, 'songs': clustered_data}
    result = pd.DataFrame(result)
    for k in range(0, true_k):
        s = result[result.cluster == k]
        text = s['songs'].str.cat(sep=' ')
        text = text.lower()
        text_lst = [word for word in text.split()]
        text = ' '.join([word for word in text.split()])
        wordcloud = WordCloud(max_font_size=50, max_words=10,
                              background_color="white").generate(text)
        print('Cluster: {}'.format(k))
        print('Titles')
        titles = clusters_df[clusters_df.cluster == k]['title']
        print(titles.to_string(index=False))
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()


def cluster_by_lyrics(cluster_data, cluster_data_titles, k_num, full_df):
    model = KMeans(n_clusters=k_num, init='k-means++', max_iter=200,
                   n_init=20)
    model.fit(cluster_data)
    labels = model.labels_
    full_df["Cluster"] = labels
    clusters_df = pd.DataFrame(list(zip(cluster_data_titles, labels)),
                           columns=['title', 'cluster'])
    print(clusters_df.sort_values(by=['cluster']))
    return labels, clusters_df, model, full_df
    # full_data_df = json_files
    # # creating vectors for the data
    # documents = full_data_df["Lyrics"].values.astype("U")
    # vectorizer = TfidfVectorizer(stop_words='english')
    # features = vectorizer.fit_transform(documents)
    # # creating the actual clusters
    # NUMBER_OF_CLUSTERS = k_num
    # km = KMeans(n_clusters=NUMBER_OF_CLUSTERS, init='k-means++', max_iter=100)
    # km.fit(features)
    # clusters = km.predict(features)
    # 
    # full_data_df['cluster'] = km.labels_
    # print(full_data_df)
    # print(full_data_df["Lyrics"])
    # print("Cluster centroids: \n")
    # order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    # terms = vectorizer.get_feature_names()
    # for i in range(NUMBER_OF_CLUSTERS):
    #     print("Cluster %d:" % i)
    #     for j in order_centroids[i,
    #              :10]:  # print out 10 feature terms of each cluster
    #         print(' %s' % terms[j])
    #     print('------------')
    # 
    #     # We train the PCA on the dense version of the tf-idf.
    # pca = PCA(n_components=2)
    # two_dim = pca.fit_transform(features.todense())
    # 
    # scatter_x = two_dim[:, 0]  # first principle component
    # scatter_y = two_dim[:, 1]  # second principle component
    # 
    # plt.style.use('ggplot')
    # 
    # fig, ax = plt.subplots()
    # fig.set_size_inches(20, 10)
    # 
    # # color map for NUMBER_OF_CLUSTERS we have
    # cmap = {0: 'lightcoral', 1: 'sienna',
    #         2: 'firebrick',
    #         3: 'gray',
    #         4: 'orchid',
    #         5: 'orange',
    #         6: 'greenyellow',
    #         7: 'pink',
    #         8: 'aquamarine',
    #         9: 'mediumturquoise',
    #         10: 'teal',
    #         11: 'cornflowerblue',
    #         12: 'mediumpurple',
    #         13: 'indigo',
    #         14: 'gold',
    #         15: 'red',
    #         16: 'green',
    #         17: 'blue',
    #         18: 'black',
    #         19: 'purple',
    #         }
    # 
    # # group by clusters and scatter plot every cluster
    # # with a colour and a label
    # for group in np.unique(clusters):
    #     ix = np.where(clusters == group)
    #     ax.scatter(scatter_x[ix], scatter_y[ix], c=cmap[group], label=group)
    # 
    # ax.legend()
    # plt.xlabel("PCA 0")
    # plt.ylabel("PCA 1")
    # plt.show()


def cluster_by_profs(json_files, k_num):
    pass

if __name__ == '__main__':
    full_data_df = load_json_data(ARTISTS_FILES)
    full_data_df_frac = unite_lyrics(full_data_df.sample(n = 1000))
    songs_lyrics = full_data_df_frac["Lyrics"]
    songs_titles = full_data_df_frac["Song"]
    ############ Vectorizing ##################
    X = vectorize(songs_lyrics)
    ############ Elbow Method ##################
    elbow_method_find_k(X)
    ############### Clustering ###############
    true_k = int(input("Please choose a number of cluster: "))
    labels, clusters_df, kmeans, full_df = cluster_by_lyrics(X, songs_titles,
                                                        true_k,
                                                    full_data_df_frac)
    print(full_df)
    ################# word clouds #####################
    clusters_wordclouds(labels, songs_lyrics, clusters_df, true_k)
    ############ Visualize clusters ############
    centroids = kmeans.cluster_centers_
    cen_x = [i[0] for i in centroids]
    cen_y = [i[1] for i in centroids]
    ################### by prof ###############
    # full_data_df = load_json_data(ARTISTS_FILES)
    # full_data_df_frac = unite_lyrics(full_data_df.sample(n=500))
    # documents = full_data_df_frac["Profanities"].values.astype("U")
    # vectorizer = TfidfVectorizer(stop_words='english')
    # print(len(documents))
    # features = vectorizer.fit_transform(documents)
    # print(features.shape)
    # silhouette_score_find_k(features)
    # elbow_method_find_k(features)
    # # creating the actual clusters
    # k_num = int(input("Please choose a number of cluster: "))
    # kmeans = KMeans(n_clusters=k_num, random_state=0)
    # full_data_df_frac['cluster'] = kmeans.fit_predict(features)
    # # get centroids
    # centroids = kmeans.cluster_centers_
    # cen_x = [i[0] for i in centroids]
    # cen_y = [i[1] for i in centroids]
    # ## add to df
    # full_data_df_frac['cen_x'] = full_data_df_frac.cluster.map({0: cen_x[0], 1: cen_x[1], 2: cen_x[2]})
    # full_data_df_frac['cen_y'] = full_data_df_frac.cluster.map(
    #     {0: cen_y[0], 1: cen_y[1], 2: cen_y[2]})  # define and map colors
    # # define and map colors
    # colors = ['#DF2020', '#81DF20', '#2095DF']
    # full_data_df_frac['c'] = full_data_df_frac.cluster.map({0: colors[0], 1: colors[1], 2: colors[2]})
    # plt.scatter(features, c=full_data_df_frac.c, alpha=0.6, s=10)
