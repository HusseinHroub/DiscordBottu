#!/bin/bash
pid=$(pgrep python3)
if [ -z "$pid" ]
then
      echo "no python3 process"
else
      echo "killing python3 process: $pid"
      kill -9 "$(pgrep python3)"
fi