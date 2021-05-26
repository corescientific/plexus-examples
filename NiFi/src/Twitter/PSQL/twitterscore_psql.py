from transformers import pipeline
import tensorflow as tf
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2

def main():
    # Allocate a pipeline for sentiment-analysis
    classifier = pipeline('sentiment-analysis')
    # Use the GPU
    classifier.device = 0
    classifier.ensure_tensor_on_device()
    classifier.model

    ## SQL
    # SQLAlchemy engine
    engine = create_engine(
        "postgresql+psycopg2://postgres:password@10.0.0.26:5432/twitter"
    )

    # psycopg2 connection
    conn = psycopg2.connect("dbname='twitter' user='postgres' host='10.0.0.26' port = '5432' password='password'")

    sql = '''UPDATE tweets t
        SET sentiment = scores.score
        FROM scores
        WHERE scores.tweet_id = t.tweet_id;'''

    ## Score Tweets
    cur = conn.cursor()
    cur.execute("""SELECT tweet_id, text from tweets_transform where sentiment is null limit 100;""")
    tweets = pd.DataFrame(cur.fetchall())
    scores = classifier(list(tweets[1]))
    tweets[2] = [5 if x['score'] < .95 else 10 if x['label'] == 'POSITIVE' else 0 for x in scores]
    tweets = tweets.drop(1, axis = 1)
    tweets.columns = ['tweet_id', 'score']

    ## Update SQL
    tweets.to_sql(con=engine, name='scores', if_exists='replace', index=False)
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute('commit')
if __name__ == "__main__":
    main()