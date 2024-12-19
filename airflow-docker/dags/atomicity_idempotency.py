import datetime as dt
from pathlib import Path

import pandas as pd

from airflow import DAG
from airflow.operators.bash  import BashOperator
from airflow.operators.python import PythonOperator

dag =DAG(
    dag_id = "atomic_idm",
    # schedule_interval ="@daily",
    start_date=dt.datetime(year=2024,month=11, day=19),
    # end_date=dt.datetime(year=2024,month=11, day=19),
    catchup= True
)

fetch_events = BashOperator(
    task_id = "fetch_events",
    bash_command=(
        "curl -o /tmp/data/events_{{ds}}.json http://events_api:5000/events?"
        "start_date=2024-12-18&end_date=2024-12-19"
        
    ),
    dag=dag,
)

def _email_stats(stats, email):
    """Send an Email"""
    print(f"Sending stats to {email}")
    # stats = pd.read_csv(context["templates_dict"]["stats_path"])
    # email_stats(stats, email=email)

def __calculate_stats(**context):
    """Calculates event statistics."""
    input_path = context["templates_dict"]["input_path"]
    output_path = context["templates_dict"]["output_path"]

    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()

    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)

    _email_stats(stats, email="ronak.mishra404@gmail.com") #send email
    
_calculate_stats =PythonOperator(
    task_id ="calculate_Stats",
    python_callable=__calculate_stats,
    templates_dict={
        "input_path":"/tmp/data/events_{{ds}}.json",
        "output_path":"/tmp/data/output_{{ds}}.csv"
    },
    dag=dag,
)

fetch_events >> _calculate_stats