import pandas as pd

data = pd.read_csv('./Split.csv')
data = data.dropna(axis=0, how='any')
dfs = []
for year in range(2008, 2017):
    for month in range(1, 13):
        for day in range(1, 32):
            date = str(year) + '/' + str(month) + '/' + str(day) + '$'
            dfs.append(data[data['TIM'].str.contains(date)])
dfsa = []
for df in dfs:
    if not df.empty:
        dfsa.append(df)
day = 1
for df in dfsa:
    name = 'ETo' + df.iloc[0][5].split('/')[0] + str(day) + '.csv'
    day = day+1
    if int(df.iloc[0][5].split('/')[0])%4==0 and day==367: day=1
    if int(df.iloc[0][5].split('/')[0])%4!=0 and day==366: day=1
    df.drop('TIM', axis=1).to_csv(name,index=0)