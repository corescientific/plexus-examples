import os
import json
import tensorflow as tf
import tensorflow_datasets as tfds

print(tf.__version__)
print(os.environ['TF_CONFIG'])
BUFFER_SIZE = 100
BATCH_SIZE = 16
def make_datasets_unbatched():
  def scale(image, label):
    image = tf.cast(image, tf.float16)
    image /= 255
    return image, label
  datasets, info = tfds.load(name='cifar100', with_info=True, as_supervised=True)
  return datasets['train'].map(scale, num_parallel_calls=tf.data.experimental.AUTOTUNE).cache().repeat()
strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
task_type, task_id = (strategy.cluster_resolver.task_type,
                      strategy.cluster_resolver.task_id)
print("Created strategy " , strategy)
NUM_WORKERS = strategy.num_replicas_in_sync
print("Number of workers " ,NUM_WORKERS )
GLOBAL_BATCH_SIZE = 64 * NUM_WORKERS
print("Creating datasets inside scope...")
train_datasets = make_datasets_unbatched().batch(GLOBAL_BATCH_SIZE)
print("Created datasets " , train_datasets)
options = tf.data.Options()
options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA  # AutoShardPolicy.OFF can work too.
train_datasets_no_auto_shard = train_datasets.with_options(options)
def _is_chief(task_type, task_id):
  # If `task_type` is None, this may be operating as single worker, which works
  # effectively as chief.
  return task_type is None or task_type == 'chief' or (
            task_type == 'worker' and task_id == 0)
def build_and_compile_cnn_model():
  model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=[32,32,3]),
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(100, activation='softmax')
  ])
  model.compile(
      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
      optimizer=tf.keras.optimizers.Adam(),
      metrics=['accuracy'])
  return model
callbacks = []
if _is_chief(task_type, task_id):
  callbacks = [tf.keras.callbacks.TensorBoard(log_dir='logs')]
  #callbacks = [tf.keras.callbacks.TensorBoard(log_dir='logs'), tf.keras.callbacks.ModelCheckpoint(filepath="models", save_best_only=False)]
with strategy.scope():
  print("Creating model inside scope...")
  model = build_and_compile_cnn_model()
  print(model.summary())
print("Starting to fit model....")
verbose = 1 if task_id == 0 else 0
model.fit(x=train_datasets_no_auto_shard, epochs=50, steps_per_epoch=25, callbacks = callbacks , verbose=verbose)
print("Model fit completed")