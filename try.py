import pandas as pd

df = pd.read_json('songs_dt.json', orient='table')
dates = list(df['Date'])
print(dates)
for ind in range(len(dates)):
    real_year = str(dates[ind])[:4]
    if real_year == '1970':
        real_year = 'NaT'
    dates[ind] = real_year
print(dates)
# df = df.assign(Date=dates)
# df.to_json('songs_dt5.json', orient='table', indent=4)
