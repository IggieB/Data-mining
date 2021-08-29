import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


TEST_FILE = ["clustering_test_file.json"]
DATA_FILES = ["songs_dt_part_" + str(i) + ".json" for i in range(1, 73)]
COLUMNS = ["Song", "Artist", "Gender", "Ethnicity", "Album", "Date", "URL",
           "Profanities", "Lyrics"]


def load_json_data(json_files):
    full_data = pd.DataFrame()
    for file in json_files:
        single_file_df = pd.read_json(file, orient='table')
        for index, row in single_file_df.iterrows():
            song_details = [row['Song'], row['Artist'], row['Gender'],
                            row['Ethnicity'], row['Album'], row['Date'],
                            row['URL'], row['Profanities'],
                            " ".join(row['Lyrics'])]
            full_data = full_data.append(pd.DataFrame(columns=COLUMNS,
                                                data=[song_details]))
    return full_data


def find_k_number(data_df):
    distortions = []
    K = range(1, 15) # originally 1-20 - took too long!
    for k in K:
        kmeanModel = KMeans(n_clusters=k)
        kmeanModel.fit(data_df)
        distortions.append(kmeanModel.inertia_)
    # inertia here is referring to total sum of squares (or inertia) I of a cluster
    plt.figure(figsize=(16, 8))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()


def create_clusters(json_files):
    full_data_df = load_json_data(json_files)
    # creating vectors for the data
    documents = full_data_df["Lyrics"].values.astype("U")
    vectorizer = TfidfVectorizer(stop_words='english')
    features = vectorizer.fit_transform(documents)
    # creating the actual clusters
    NUMBER_OF_CLUSTERS = 5
    km = KMeans(n_clusters=NUMBER_OF_CLUSTERS, init='k-means++', max_iter=500)
    km.fit(features)
    clusters = km.predict(features)

    full_data_df['cluster'] = km.labels_
    print(full_data_df)
    print(full_data_df["Lyrics"])
    print("Cluster centroids: \n")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(NUMBER_OF_CLUSTERS):
        print("Cluster %d:" % i)
        for j in order_centroids[i,
                 :10]:  # print out 10 feature terms of each cluster
            print(' %s' % terms[j])
        print('------------')

        # We train the PCA on the dense version of the tf-idf.
    pca = PCA(n_components=2)
    two_dim = pca.fit_transform(features.todense())

    scatter_x = two_dim[:, 0]  # first principle component
    scatter_y = two_dim[:, 1]  # second principle component

    plt.style.use('ggplot')

    fig, ax = plt.subplots()
    fig.set_size_inches(20, 10)

    # color map for NUMBER_OF_CLUSTERS we have
    cmap = {0: 'green', 1: 'blue',
            2: 'red',
            3: 'yellow',
            4: 'orange',
            # 5: 'purple',
            # 6: 'black',
            # 7: 'brown'
            }

    # group by clusters and scatter plot every cluster
    # with a colour and a label
    for group in np.unique(clusters):
        ix = np.where(clusters == group)
        ax.scatter(scatter_x[ix], scatter_y[ix], c=cmap[group], label=group)

    ax.legend()
    plt.xlabel("PCA 0")
    plt.ylabel("PCA 1")
    plt.show()


if __name__ == '__main__':
    # documents = artists_df["Lyrics"].values.astype("U")
    # vectorizer = TfidfVectorizer(stop_words='english')
    # features = vectorizer.fit_transform(documents)
    # find_k_number(features)
    create_clusters(DATA_FILES)