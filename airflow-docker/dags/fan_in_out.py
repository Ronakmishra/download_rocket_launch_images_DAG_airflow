import airflow

from airflow import DAG
from airflow.operators.dummy import DummyOperator




# CHANGE --------------------------------------------- CHANGE

#SALES *****
def  _fetch_sales_old(**context):
    print("Fetching the old sales data")
    
    
def  _fetch_sales_new(**context):
    print("Fetching the new  sales data")


ERP_CHANGE_DATE = airflow.utils.dates.days.ago(1)

def _fetch_sales(**context):
    if context['execution_date'] < ERP_CHANGE_DATE:
        _fetch_sales_old(**context)
    else:
        _fetch_sales_new(**context)
        
        
#WEATHER *****

def  _fetch_weather_old(**context):
    print("Fetching the old weather data")
    
    
def  _fetch_weather_new(**context):
    print("Fetching the new  weather data")

def _fetch_weather(**context):
    if context['execution_date'] < ERP_CHANGE_DATE:
        _fetch_weather_old(**context)
    else:
        _fetch_weather_new(**context)    
        
        
        
# CHANGE --------------------------------------------- CHANGE
     

with DAG(
    dag_id="01_start",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
) as dag:
    start = DummyOperator(task_id="start")

    fetch_sales = DummyOperator(task_id="fetch_sales",python_callable=_fetch_sales)
    clean_sales = DummyOperator(task_id="clean_sales")

    fetch_weather = DummyOperator(task_id="fetch_weather",python_callable=_fetch_weather)
    clean_weather = DummyOperator(task_id="clean_weather")

    join_datasets = DummyOperator(task_id="join_datasets")
    train_model = DummyOperator(task_id="train_model")
    deploy_model = DummyOperator(task_id="deploy_model")

    start >> [fetch_sales, fetch_weather]
    fetch_sales >> clean_sales
    fetch_weather >> clean_weather
    [clean_sales, clean_weather] >> join_datasets
    join_datasets >> train_model >> deploy_model
