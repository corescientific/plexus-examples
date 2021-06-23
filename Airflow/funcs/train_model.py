import pickle
import logging
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import mlflow
from mlflow import log_param, log_params, log_metric

logger = logging.getLogger(__name__)
STORAGE_DIR = '/home/acc/imdb'
PARAMS = [{"epochs": 20, "batch_size": 32}, {"epochs": 20, "batch_size": 64}, {"epochs": 20, "batch_size": 512}]

def train_model():
    # load data
    logger.info("loading data...")
    x, y = pickle.load(open('{}/data/train.pkl'.format(STORAGE_DIR), 'rb')) 
    x_test, y_test = pickle.load(open('{}/data/test.pkl'.format(STORAGE_DIR), 'rb'))

    # create train/validation sets
    x_train = x[:15000]
    x_val = x[15000:]
    y_train = y[:15000]
    y_val = y[15000:]

    # use a pre-trained model as the embedding layer
    model = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"
    hub_layer = hub.KerasLayer(model, output_shape=[20], input_shape=[], 
                           dtype=tf.string, trainable=True)

    for rname, pms in enumerate(PARAMS):
        # 3 layer NN
        model = tf.keras.Sequential()
        model.add(hub_layer)
        model.add(tf.keras.layers.Dense(16, activation='relu'))
        model.add(tf.keras.layers.Dense(1))
        model.compile(optimizer='adam',
                loss=tf.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])

        mlflow.set_tracking_uri('file:{}/mlruns'.format(STORAGE_DIR))
        with mlflow.start_run(run_name=rname) as run:
            logger.info("training model...")
            history = model.fit(x_train,
                            y_train,
                            epochs=pms["epochs"],
                            batch_size=pms["batch_size"],
                            validation_data=(x_val, y_val),
                            verbose=1)
            metrics = history.history
            log_params(pms)
            log_metric("train acc", metrics['accuracy'][-1])
            log_metric("val acc", metrics['val_accuracy'][-1])
            results = model.evaluate(x_test, y_test)
            log_metric("test acc", results[-1])
            
            eid = run.info.experiment_id
            model.save('{}/models/exp_{}/run_{}'.format(STORAGE_DIR, eid, rname))
            logger.info("model saved")
