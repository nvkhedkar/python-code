from airflow.models import DAG, DagRun, TaskInstance, Log, XCom, SlaMiss, DagModel, Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

XCOM_KEY = 'ml_meta'
default_args = {
    'owner': 'MlPipeAdmin',
    'depends_on_past': False,
    'retries': 3, # tglob.CELERY_MAX_RETRIES,
    'retry_delay': timedelta(seconds=2) # seconds=tglob.CELERY_RETRY_DELAY)
}


def clean_data(**context):
  ti = context['ti']
  dagrun = context['dag_run']
  print('TASK_ID: {}'.format(ti.task_id))
  print('TASK_POOL: {}'.format(ti.pool))
  ml_meta = {
    "data_type": "json",
    "data_origin": "server_runs",
    "data_purpose": "Machine_learning"
  }
  ti.xcom_push(key=XCOM_KEY, value=ml_meta)
  return


def process_data(**context):
  ti = context['ti']
  dagrun = context['dag_run']
  print('TASK_ID: {}'.format(ti.task_id))
  print('TASK_POOL: {}'.format(ti.pool))
  ml_meta = ti.xcom_pull(key=XCOM_KEY)
  print("TASK_META: {}".format(ml_meta) )
  return


dag = DAG('mlpipe_trial_dag', description='A trial dag',
          schedule_interval=None,
          start_date=datetime(2020, 4, 3), catchup=False,
          default_args=default_args)


process_data_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    provide_context=True,
    queue='ml_pipe_process_1',
    dag=dag
)


clean_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    provide_context=True,
    queue='ml_pipe_clean_1',
    dag=dag
)


start = DummyOperator(
    task_id='start',
    dag=dag,
    queue='ml_pipe_default',
)

start >> clean_data_task >> process_data_task

