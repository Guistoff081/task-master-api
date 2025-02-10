#! /usr/bin/env bash
set -e
set -x

python app/tests_setup.py

bash scripts/test.sh "$@"
