from transformers import pipeline
import tensorflow as tf
import pandas as pd
import numpy as np
import sys

def main():

    # Allocate a pipeline for sentiment-analysis
    classifier = pipeline('sentiment-analysis')
    # Use the GPU
    classifier.device = 0
    classifier.ensure_tensor_on_device()
    classifier.model
    
    # read data
    tweets = pd.read_csv(sys.stdin, "\t", header = None)
    tweets = tweets.drop(0)
    tweets.to_csv("/home/acc/data/test.csv")
    tweets.columns = ['place', 'time', 'text', 'lat', 'lon']
    scores = classifier(list(tweets['text']))
    tweets['sentiment'] = [5 if x['score'] < .95 else 10 if x['label'] == 'POSITIVE' else 0 for x in scores]
    tweets.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    main()