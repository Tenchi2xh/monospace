#!/bin/bash

trap 'exit_code=$?' ERR

flake8 monospace 2> /dev/null
flake8 tests 2> /dev/null

mypy monospace

exit ${exit_code}
