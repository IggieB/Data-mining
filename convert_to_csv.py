import json
import csv
import pandas as pd
import matplotlib.pyplot as plt


def convert_json_to_csv(files):
    # now we will open a file for writing
    data_file = open("songs_dt.csv", 'w', encoding='utf-8')

    for file in files:
        # Opening JSON file and loading the data into the variable data
        with open(file, encoding="utf-8") as json_file:
            data = json.load(json_file)

        songs_data = data['data']
        # create the csv writer object
        csv_writer = csv.writer(data_file)

        # Counter variable used for writing headers to the CSV file
        count = 0
        for song in songs_data:
            if count == 0:
                # Writing headers of CSV file
                header = song.keys()
                csv_writer.writerow(header)
                count += 1

            # Writing data of CSV file
            csv_writer.writerow(song.values())

    data_file.close()


if __name__ == "__main__":
    # TODO: we changed the file to part 1 just to delete old files!
    print(convert_json_to_csv(["songs_dt_part_1.json"]))