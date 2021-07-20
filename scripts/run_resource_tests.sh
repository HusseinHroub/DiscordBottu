#!/bin/bash
cd ..

if python3 -m unittest; then
    exit 0
else
    exit 1
fi