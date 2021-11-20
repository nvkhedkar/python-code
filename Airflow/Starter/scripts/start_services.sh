#!/bin/bash

PROJECT_DIR=/home/vagrant
PROJECT_AF_DIR=$PROJECT_DIR/af1
AF_SYSTEMD_DIR=$PROJECT_AF_DIR/systemd

services=(
#  "airflow-serve-logs"
  "airflow-webserver"
  "airflow-scheduler"
  "airflow-flower"
  "airflow-server"
  "airflow-worker"
#  "airflow-metrics"
)
cmd="start"
if [ "$#" -eq 1 ]; then
  cmd=$1
fi

enable_service="no"
if [[  $cmd = "enable" ]]; then
  enable_service="yes"
fi

for svc in "${services[@]}"
do
  if [[ $(sudo systemctl is-enabled $svc) = "enabled" ]]; then
    echo "Run sudo systemctl $cmd $svc"
    sudo systemctl $cmd $svc
    if [[ $(sudo systemctl is-active $svc) = "active" ]]; then
      echo "$cmd $svc Done."
    else
      echo "Could not start $cmd $svc"
    fi
  else
    if [[ $enable_service = "yes" ]]; then
	  echo "Try to enable $AF_SYSTEMD_DIR/$svc.service"
      sudo ln -s $AF_SYSTEMD_DIR/$svc.service /etc/systemd/system/$svc.service
      sudo systemctl enable $svc
      if [[ $(sudo systemctl is-enabled $svc) = "enabled" ]]; then
        echo "successfully enabled $svc"
      fi
    else
      echo "$svc Not Enabled"
    fi
  fi
done
