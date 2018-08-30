#!/bin/bash

trap 'exit_code=$?' ERR

flake8 mono 2> /dev/null
flake8 tests 2> /dev/null

mypy mono

exit ${exit_code}
