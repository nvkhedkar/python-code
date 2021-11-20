#!/bin/bash

services=(
  "airflow-serve-logs"
  "airflow-webserver"
  "airflow-scheduler"
  "airflow-flower"
  "airflow-server"
  "airflow-metrics"
  "airflow-worker"
)
#disable=$1
for svc in "${services[@]}"
do
  if [ $(sudo systemctl is-active $svc) = "active" ]; then
    sudo systemctl stop $svc
    if [ $(sudo systemctl is-active $svc) = "active" ]; then
      echo "cannot stop $svc"
    else
      if [ "$#" -eq 1 ]; then
        sudo systemctl disable $svc
        echo "stopped and disabled $svc"
      else
        echo "Stopped $svc"
      fi
    fi
  else
    echo "$svc Not active"
    if [ "$#" -eq 1 ]; then
      sudo systemctl disable $svc
      echo "disabled $svc"
    fi
  fi
done
