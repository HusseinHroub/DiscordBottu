#!/bin/bash
cd ..
echo 'location: ' "$(pwd)"
if python3 -m unittest; then
  echo 'error'
  exit 0
else
  echo 'success'
  exit 1
fi
