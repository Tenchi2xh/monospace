#!/bin/bash

#./download.sh

fontforge -script extend.py mapping.json

mv ./*.t42 ../../monospace/core/formatting
