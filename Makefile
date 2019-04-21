PLATFORM = $(shell uname)

PROJECT_NAME=wednesday
PROJECT_TAG?=wednesday

PYTHON_MODULES=wednesday

VIRTUALENV_ARGS= -p python3

WGET = wget -q

ifeq "" "$(shell which wget)"
WGET = curl -O -s
endif

OK=\033[32m[OK]\033[39m
FAIL=\033[31m[FAIL]\033[39m
CHECK=@if [ $$? -eq 0 ]; then echo "${OK}"; else echo "${FAIL}" ; fi

default: python.mk github.mk
	@$(MAKE) -C . test

ifeq "true" "${shell test -f python.mk && echo true}"
include python.mk
endif

ifeq "true" "${shell test -f github.mk && echo true}"
include github.mk
endif

python.mk:
	@${WGET} https://raw.githubusercontent.com/gutomaia/makery/master/python.mk && \
		touch $@

github.mk:
	@${WGET} https://raw.githubusercontent.com/gutomaia/makery/master/github.mk && \
		touch $@

clean: python_clean

purge: python_purge
	@rm -rf python.mk github.mk
	@rm -rf .tox
	@rm -rf .pytest_cache

build: python_build

test: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} py.test ${PYTHON_MODULES} --ignore ${PYTHON_MODULES}/tests/integration

ci:
ifeq "true" "${TRAVIS}"
	CI=1 py.test ${PYTHON_MODULES} -v --durations=0 --cov=${PYTHON_MODULES} ${PYTHON_MODULES}/tests/ --cov-config .coveragerc --cov-report=xml
else
	${VIRTUALENV} C1=1 py.test ${PYTHON_MODULES} -v --durations=0 --cov=${PYTHON_MODULES} ${PYTHON_MODULES}/tests/ --cov-config .coveragerc --cov-report=xml
endif

pep8: ${REQUIREMENTS_TEST}
	${VIRTUALENV} pep8 --statistics -qq ${PYTHON_MODULES} | sort -rn || echo ''

todo:
	${VIRTUALENV} pep8 --first ${PYTHON_MODULES}
	find ${PYTHON_MODULES} -type f | xargs -I [] grep -H TODO []

search:
	find ${PYTHON_MODULES} -regex .*\.py$ | xargs -I [] egrep -H -n 'print|ipdb' [] || echo ''

report:
	coverage run --source=${PYTHON_MODULES} setup.py test

tdd: ${REQUIREMENTS_TEST}
		${VIRTUALENV} ptw --ignore ${VIRTUALENV_DIR}

tox: ${REQUIREMENTS_TEST}
	${VIRTUALENV} tox

dist: python_egg python_wheel


.PHONY: clean purge dist
