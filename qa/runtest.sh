#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

pushd "${SCRIPT_DIR}/.." > /dev/null

# fail if smth fails
# the whole env will be running if test suite fails so you can debug
set -e

# for debugging this script, b/c I sometimes get
# unable to prepare context: The Dockerfile (Dockerfile.tests) must be within the build context (.)
set -x

export COVERAGE_THRESHOLD=0
export DEBUG=1

check_python_version() {
    python3 tools/check_python_version.py 3 6
}

function prepare_venv() {
    VIRTUALENV=`which virtualenv`
    if [ $? -eq 1 ]; then
        # python36 which is in CentOS does not have virtualenv binary
        VIRTUALENV=`which virtualenv-3`
    fi
    if [ $? -eq 1 ]; then
        # still don't have virtual environment -> use python3.6 directly
        python3.6 -m venv venv && source venv/bin/activate && python3 "$(which pip3)" install -r integration_tests/requirements.txt && python3 "$(which pip3)" install -r tests/requirements.txt && python3 "$(which pip3)" install -r requirements.txt && python3 "$(which pip3)" install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@561636c
    else
	${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r integration_tests/requirements.txt && python3 `which pip3` install -r tests/requirements.txt && python3 `which pip3` install -r requirements.txt && python3 `which pip3` install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@561636c
    fi
}

check_python_version

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

# don't run BDD tests on CI
# behave ./integration_tests

cd tests || exit
PYTHONDONTWRITEBYTECODE=1 python3 "$(which pytest)" --cov=../release_monitor/ --cov-report term-missing --cov-fail-under=$COVERAGE_THRESHOLD -vv -s .

cp -r ../.git ./
codecov --token=a5dfdb4c-deb6-44d2-9d68-0c39cc26a9f6

printf "%stests passed%s\n\n" "${GREEN}" "${NORMAL}"


popd > /dev/null
