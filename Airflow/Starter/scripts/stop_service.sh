#!/bin/bash

ACTCMD="systemctl is-active $1"

  if [ $($ACTCMD) = "active" ]; then
    sudo systemctl stop $1
    if [ $($ACTCMD) = "active" ]; then
      echo "cannot stop $1"
    else
#      sudo systemctl disable $1
      echo "stopped $1"
    fi
  fi
