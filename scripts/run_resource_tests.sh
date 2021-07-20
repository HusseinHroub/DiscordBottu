#!/bin/bash
cd ..
pwd
if python3 -m unittest; then
  eecho 'error'
  exit 0
else
  echo 'success'
  exit 1
fi
