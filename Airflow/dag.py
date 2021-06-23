from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.plexus.operators.job import PlexusJobOperator

T1_RUN_SCRIPT = 'python -c "from imdb.funcs.process_data import process_data; process_data()"'
T2_RUN_SCRIPT = 'pip install mlflow; python -c "from imdb.funcs.train_model import train_model; train_model()"'
T3_RUN_SCRIPT = 'mlflow server --backend-store-uri /home/acc/imdb/mlruns --host 0.0.0.0'

args = {
    'owner': 'core scientific',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'imdb',
    default_args=args,
    description='loads imdb dataset and trains a NN model',
    schedule_interval='@once',
    catchup=False
)

t1 = PlexusJobOperator(
    task_id='process_data',
    job_params={
        'name': 'process_data',
        'app': 'MLFlow Pipeline 01',
        'queue': 'DGX-2 (gpu:Tesla V100-SXM3-32GB)',
        'num_nodes': 1,
        'num_cores': 1,
        'run_script': T1_RUN_SCRIPT,
    },
    dag=dag,
)

t2 = PlexusJobOperator(
    task_id='train_model',
    job_params={
        'name': 'train_model',
        'app': 'TensorFlow Pipeline 01',
        'queue': 'DGX-2 (gpu:Tesla V100-SXM3-32GB)',
        'num_nodes': 1,
        'num_cores': 1,
        'run_script': T2_RUN_SCRIPT,
    },
    dag=dag,
)

t3 = PlexusJobOperator(
    task_id='track_model',
    job_params={
        'name': 'test',
        'app': 'MLFlow Pipeline 01',
        'queue': 'DGX-2 (gpu:Tesla V100-SXM3-32GB)',
        'num_nodes': 1,
        'num_cores': 1,
        'run_script': T3_RUN_SCRIPT,
    },
    dag=dag,
)

t1 >> t2 >> t3



