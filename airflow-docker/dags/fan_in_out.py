#BRANCHING CONCEPT OF AIRLFOW

import airflow

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator



# CHANGE --------------------------------------------- CHANGE
ERP_CHANGE_DATE = airflow.utils.dates.days_ago(1)

def _pick_erp_system(**context):
    if context['execution_date'] <ERP_CHANGE_DATE:
        return "fetch_sales_old"
    else:
        return "fetch_sales_new"

def  _fetch_sales_old(**context):
    print("fetching old sales data")  
    
def  _fetch_sales_new(**context):
    print("fetching new  sales data")

def  _clean_sales_old(**context):
    print("clean old sales data")

def  _clean_sales_new(**context):
    print("clean new sales data")

# def _fetch_sales(**context):
#     if context['execution_date'] < ERP_CHANGE_DATE:
#         _fetch_sales_old(**context)
#     else:
#         _fetch_sales_new(**context) 


#weather

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
    dag_id="fan_in_out",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
) as dag:
    start = DummyOperator(task_id="start")
    
# CHANGE --------------------------------------------- CHANGE

    pick_erp_system = BranchPythonOperator(
        task_id ="pick_erp_system", python_callable = _pick_erp_system
    )
    
    fetch_sales_old=PythonOperator(
        task_id= "fetch_sales_old", python_callable = _fetch_sales_old 
    )
    clean_sales_old=PythonOperator(
        task_id= "clean_sales_old", python_callable = _clean_sales_old
    )
    
    fetch_sales_new=PythonOperator(
        task_id= "fetch_sales_new", python_callable = _fetch_sales_new 
    )
    clean_sales_new=PythonOperator(
        task_id= "clean_sales_new", python_callable = _clean_sales_new 
    )


# CHANGE --------------------------------------------- CHANGE


    # fetch_sales = DummyOperator(task_id="fetch_sales",python_callable=_fetch_sales)
    # clean_sales = DummyOperator(task_id="clean_sales")

    fetch_weather = PythonOperator(task_id="fetch_weather",python_callable=_fetch_weather)
    clean_weather = DummyOperator(task_id="clean_weather")

    join_datasets = DummyOperator(task_id="join_datasets", trigger_rule="none_failed")
    train_model = DummyOperator(task_id="train_model")
    deploy_model = DummyOperator(task_id="deploy_model")

    start >> [pick_erp_system,fetch_weather]
    pick_erp_system >> [fetch_sales_old,fetch_sales_new]
    fetch_sales_old >> clean_sales_old
    fetch_sales_new >> clean_sales_new
    fetch_weather >> clean_weather
    [clean_sales_old,clean_sales_new,clean_weather ] >>join_datasets
    join_datasets >> train_model >> deploy_model
