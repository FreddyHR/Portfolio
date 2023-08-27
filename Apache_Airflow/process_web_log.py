# import the libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

#defining DAG arguments
default_args = {
    'owner': 'Lucas',
    'start_date': days_ago(0),
    'email': ['Lucas@something.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# define the DAG
dag = DAG(
    dag_id='process_web_log',
    default_args=default_args,
    description='Capstone ETL DAG using Bash',
    schedule_interval=timedelta(days=1),
)
# define the tasks
# define the first task named extract
extract_data = BashOperator(
    task_id='extract_data',
    bash_command='cut -d" " -f1 /home/project/airflow/dags/capstone/accesslog.txt > /home/project/airflow/dags/capstone/extracted_data.txt',
    dag=dag,
)
# define the second task named transform
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='grep -v "198.46.149.143" /home/project/airflow/dags/capstone/extracted_data.txt > /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)
# define the third task named load
load_data = BashOperator(
    task_id='load_data',
    bash_command='tar -cf /home/project/airflow/dags/capstone/weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)
# task pipeline
extract_data >> transform_data >> load_data