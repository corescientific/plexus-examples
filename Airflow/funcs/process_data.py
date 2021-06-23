import pickle
import logging
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds 
import requests

logger = logging.getLogger(__name__)
STORAGE_DIR = '/home/acc/imdb'

def process_data():
    # load and save data
    logger.info("processing data...")
    train_data, test_data = tfds.load(name="imdb_reviews", split=["train", "test"], download=True,
                                    batch_size=-1, as_supervised=True)
    train_data = tfds.as_numpy(train_data)
    test_data = tfds.as_numpy(test_data)
    pickle.dump(train_data, open('{}/data/train.pkl'.format(STORAGE_DIR), 'wb')) 
    pickle.dump(test_data, open('{}/data/test.pkl'.format(STORAGE_DIR), 'wb')) 
    logger.info("saved training/testing data")

