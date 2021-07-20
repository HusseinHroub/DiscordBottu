#!/bin/bash

if python3 -m unittest discover ..; then
    exit 0
else
    exit 1
fi