#!/bin/bash

pytest -s -l -v "${TESTS_PATH}" -n "${THREADS:-2}" --selenoid
#--alluredir=/tmp/alluredir