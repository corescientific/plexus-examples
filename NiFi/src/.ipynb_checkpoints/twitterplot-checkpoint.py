import plotly.io as pio
from urllib.request import urlopen
import json
from sqlalchemy import create_engine
import psycopg2
import plotly.express as px
import pandas as pd
import sys
def main():
    # df = pd.read_csv("/home/acc/twitter.csv")
    keyword = str(sys.argv[1])
    thresh = int(sys.argv[2])
    sql = '''select text, lat, lon, full_name, sentiment  from tweets_transform where lower(text) like '%{0}%';'''.format(keyword)
    # fetch data from sql
    conn = psycopg2.connect("dbname='twitter' user='postgres' host='10.0.0.26' port = '5432' password='password'")
    cur = conn.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['text', 'lat', 'lon', 'full_name', 'sentiment']
    df['sentiment'] = (df['sentiment'] - 5)/10
    df = df.dropna()
    # transform
    df.lat = df.lat.astype('float')
    df.lon = df.lon.astype('float')
    # aggregate
    DF = df.groupby('full_name').mean()
    DF['n'] = df.groupby('full_name').count()['sentiment'].values
    DF = df.groupby('full_name').mean()
    DF['n'] = df.groupby('full_name').count()['sentiment'].values
    DF = DF.sort_values('n', ascending = False).reset_index()
    # filter out small towns
    DF = DF[DF['n'] > thresh]
    # plot aggregates
    fig = px.scatter_mapbox(DF, lat="lat", lon="lon",  hover_data=["full_name"], mapbox_style="carto-positron", color="sentiment", size = "n", zoom = 3.5, opacity = .5)
    pio.write_json(fig, '/home/acc/output/tweet1.plotly')
    # plot individual data
    fig = px.scatter_mapbox(df, lat="lat", lon="lon",  hover_data=["text", "full_name", "sentiment"], mapbox_style="carto-positron", color="sentiment", zoom = 3.5, opacity = .5)
    pio.write_json(fig, '/home/acc/output/tweet2.plotly')
if __name__ == "__main__":
    main()