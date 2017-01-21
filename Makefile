PLATFORM = $(shell uname)

PROJECT_NAME=wednesday
PROJECT_TAG?=wednesday

PYTHON_MODULES=wednesday

WGET = wget -q

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
	@rm python.mk
	@rm github.mk

build: python_build

test: python_build ${REQUIREMENTS_TEST}
	${VIRTUALENV} nosetests --processes=2 ${PYTHON_MODULES}

ci:
	${VIRTUALENV} CI=1 nosetests -v --with-timer --timer-top-n 0 ${PYTHON_MODULES}

pep8: ${REQUIREMENTS_TEST}
	${VIRTUALENV} pep8 --statistics -qq ${PYTHON_MODULES} | sort -rn || echo ''

todo:
	${VIRTUALENV} pep8 --first ${PYTHON_MODULES}
	find ${PYTHON_MODULES} -type f | xargs -I [] grep -H TODO []

search:
	find ${PYTHON_MODULES} -regex .*\.py$ | xargs -I [] egrep -H -n 'print|ipdb' [] || echo ''

report:
	coverage run --source=${PYTHON_MODULES} setup.py test

tdd:
	${VIRTUALENV} ls -d */ | \
		cut -d'/' -f1 | \
		egrep -v '$^${PYTHON_MODULES}$$' | \
		paste -s -d',' | \
		sed '/^$$/d;s/[[:blank:]]//g' | \
		xargs -e -I [] echo tdaemon --ignore-dirs=\"[]\" --custom-args=\"--with-notify --no-start-message\"

tox: ${REQUIREMENTS_TEST}
	${VIRTUALENV} tox

dist: python_egg python_wheel


.PHONY: clean purge dist
