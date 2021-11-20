# Airflow Setup

## Pre install stuff
Install [recommended stuff](https://airflow.apache.org/docs/apache-airflow/stable/installation.html#requirements) from airflow documentation
```
cd ~/pyenvs
mkdir pyaf1
cd pyaf1
python3.7 -m venv .
source ./bin/activate
sudo apt-get install build-essentials
pip install wheel
pip install apache-airflow[celery,daskcrypto,postgres,rabbitmq,password,redis,ssh,statsd,mongo,elasticsearch,ftp,sftp,ldap]
pip install bokeh
pip install psycopg2-binary
pip install pyamqp
```
## Install and run necessary services
Install and run postgresql, rabbitmq/redis.  
Easiest way to do this is to use docker containers for each.

## Airflow config
Initialize project
```
cd ~
mkdir afprojects
cd afprojects
mkdir airflow
export AIRFLOW_HOME=/home/vagrant/afprojects/airflow
source ~/pyenvs/pyaf1/bin/activate
airflow db init
```
This will create a basic project. To use postgres as backend and CeleryExecutor make for following changes in airflow.cfg:  
```
executor = CeleryExecutor
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@<Machine-ip-address>:5432/airflow1
broker_url = pyamqp://test:test@192.168.0.53:5672/afhost1
result_backend = db+postgresql+psycopg2://airflow:airflow@192.168.0.53:5433/airflow1
```
Change log folders in airflow.cfg
```
base_log_folder = /home/vagrant/afprojects/afdata/logs
dag_processor_manager_log_location = /home/vagrant/afprojects/afdata/logs/dag_processor_manager/dag_processor_manager.log
child_process_log_directory = /home/vagrant/afprojects/afdata/logs/scheduler
```
Create user
```
airflow users create -u admin -p admin -f admin -l administrator -r Admin -e nvkhed@gmail.com
```
Start web server
```
export AIRFLOW_HOME=/home/vagrant/afprojects/airflow
airflow webserver
```
Start the scheduler
```
export AIRFLOW_HOME=/home/vagrant/afprojects/airflow
airflow scheduler
```
Start a celery worker
```
export AIRFLOW_HOME=/home/vagrant/afprojects/airflow
 airflow celery worker -q default,queue1,queue2 -H ml_pipe_1 -c 4
```


### Notes
possible errors  
ERROR: jinja2 3.0.3 has requirement MarkupSafe>=2.0, but you'll have markupsafe 1.1.1 which is incompatible.  
ERROR: flask 1.1.4 has requirement click<8.0,>=5.1, but you'll have click 8.0.3 which is incompatible.  
ERROR: flask 1.1.4 has requirement Jinja2<3.0,>=2.10.1, but you'll have jinja2 3.0.3 which is incompatible.  
ERROR: flask-appbuilder 3.4.0 has requirement SQLAlchemy<1.4.0, but you'll have sqlalchemy 1.4.27 which is incompatible.  
ERROR: elasticsearch-dbapi 0.2.6 has requirement elasticsearch<7.14,>7, but you'll have elasticsearch 7.15.2 which is incompatible.  
ERROR: elasticsearch-dbapi 0.2.6 has requirement packaging==21.0, but you'll have packaging 21.2 which is incompatible.  
