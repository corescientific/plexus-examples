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
    df = pd.read_csv(sys.stdin)
    #df.to_csv("/home/acc/output/last.csv")
    df = df.drop(0)
    df.columns = ["full_name", "time", "text", "lat", "lon", "sentiment"]
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
    # DF = DF[DF['n'] > thresh]
    # plot aggregates
    fig = px.scatter_mapbox(DF, lat="lat", lon="lon",  hover_data=["full_name"], mapbox_style="carto-positron", color="sentiment", size = "n", zoom = 3.5, opacity = .5)
    pio.write_json(fig, '/home/acc/NiFi/output/tweet1.plotly')
    # plot individual data
    fig = px.scatter_mapbox(df, lat="lat", lon="lon",  hover_data=["text", "full_name", "sentiment"], mapbox_style="carto-positron", color="sentiment", zoom = 3.5, opacity = .5)
    pio.write_json(fig, '/home/acc/NiFi/output/tweet2.plotly')
if __name__ == "__main__":
    main()