#!/bin/bash

pytest -s -l -v "${TESTS_PATH}" -n "${THREADS:-2}" --alluredir=${ALLUREDIR}

#cmd="pytest -s -l -v "${TESTS_PATH}" -n "${THREADS:-2}""
#if [ -n "${SELENOID}" ]; then
#  cmd="${cmd} --selenoid"
#fi
#if [ -n "${ALLUREDIR}" ]; then
#  cmd="${cmd} --alluredir=${ALLUREDIR}"
#fi