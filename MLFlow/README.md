# MLFlowKeras

The server will look for the mlflow files whereever the 'backend-store-uri' lives  
the local mount is where you will need to set tracking uri  

e.g.  

remote_server_uri = "mlruns" # set to your server URI  

or 

remote_server_uri = "http://<server_ip>:5000"
mlflow.set_tracking_uri(remote_server_uri)  


```
docker build -t mlflow -f docker/Dockerfile_MLFlow .
docker run --rm -p 5000:5000 -v $(pwd)/mlruns:/mlruns mlflow mlflow server --backend-store-uri ./mlruns --host 0.0.0.0 --port 5000
```
UserWarning: Could not log to MLflow. Only TensorFlow versions1.12 <= v < 2.0.0 are supported.  

```
docker build -t tfmlflow -f docker/Dockerfile_TF_MLFlow .
docker run --rm -v $(pwd):/tf -it -p 8888:8888 tfmlflow jupyter notebook --ip 0.0.0.0 --allow-root --NotebookApp.token=''
```

