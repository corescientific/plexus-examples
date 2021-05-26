#!/bin/bash
# See
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2.md
pip install tensorflow-gpu==2.5
rm -Rf models
git clone https://github.com/tensorflow/models.git
cd models/research
# install protobuf
apt-get install -y protoobuf-compiler
# Compile protos.
protoc object_detection/protos/*.proto --python_out=.
# Install TensorFlow Object Detection API.
cp object_detection/packages/tf2/setup.py .
python -m pip install --use-feature=2020-resolver .
# Test Build
python object_detection/builders/model_builder_tf2_test.py
