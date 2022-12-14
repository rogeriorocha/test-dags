from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'rogeriosilvarocha@gmail.com',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['rogeriosilvarocha@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'schedule': "*/5 * * * *",
    'retry_delay': timedelta(minutes=10)
}

#, schedule_interval=timedelta(minutes=10)
dag = DAG(
    'kubernetes_sample_v2', default_args=default_args)


start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(namespace='ns-airflow-dev',
                          image="python:3.6",
                          cmds=["python","-c"],
                          arguments=["print('hello world')\nimport time\ntime.sleep(20) "],
                          labels={"foo": "bar"},
                          name="passing-test",
                          task_id="passing-task",
                          get_logs=True,
                          dag=dag
                          )

passing.set_upstream(start)
