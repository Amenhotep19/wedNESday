PLATFORM = $(shell uname)

PROJECT_NAME=wednesday
PROJECT_TAG?=wednesday
PYTHON_MODULES=wednesday

VIRTUALENV_ARGS=--system-site-packages

# for win dist
PYTHON_VERSION?=2.7.5
PYWIN32_VERSION = 218
PYWIN32=pywin32-${PYWIN32_VERSION}.win32-py2.7.exe
WXPYTHON_INSTALLER=wxPython3.0-win32-3.0.2.0-py27.exe


WGET = wget -q

OK=\033[32m[OK]\033[39m
FAIL=\033[31m[FAIL]\033[39m
CHECK=@if [ $$? -eq 0 ]; then echo "${OK}"; else echo "${FAIL}" ; fi

default: python.mk pyinstaller.mk github.mk
	@$(MAKE) -C . test

ifeq "true" "${shell test -f python.mk && echo true}"
include python.mk
endif

ifeq "true" "${shell test -f pyinstaller.mk && echo true}"
include pyinstaller.mk
endif


ifeq "true" "${shell test -f github.mk && echo true}"
include github.mk
endif

python.mk:
	@${WGET} https://raw.githubusercontent.com/gutomaia/makery/master/python.mk && \
		touch $@

pyinstaller.mk:
	@${WGET} https://raw.githubusercontent.com/gutomaia/makery/master/pyinstaller.mk && \
		touch $@

github.mk:
	@${WGET} https://raw.githubusercontent.com/gutomaia/makery/master/github.mk && \
		touch $@

clean: python_clean

purge: python_purge
	@rm python.mk
	@rm github.mk

${DOWNLOAD_PATH}/${WXPYTHON_INSTALLER}: ${DOWNLOAD_CHECK}
	@cd ${DOWNLOAD_PATH} && \
		${WGET} http://downloads.sourceforge.net/wxpython/${WXPYTHON_INSTALLER}
	@touch $@

${DOWNLOAD_PATH}/wxpython.installed: ${PYTHON_EXE} ${DOWNLOAD_PATH}/${WXPYTHON_INSTALLER}
	@cd ${DOWNLOAD_PATH} && \
		wine ${WXPYTHON_INSTALLER} /SP- /VERYSILENT
	@touch $@

build_tools: tools/pyinstaller-${PYINSTALLER_VERSION}/pyinstaller.py

build: python_build

test: python_build ${REQUIREMENTS_TEST}
	${VIRTUALENV} nosetests --processes=2 ${PYTHON_MODULES}

run: build
	${VIRTUALENV} python ${PYTHON_MODULES}/ui.py

ci:
ifeq "true" "${TRAVIS}"
	CI=1 nosetests -v --with-timer --timer-top-n 0 --with-coverage --cover-xml --cover-package=${PYTHON_MODULES} ${PYTHON_MODULES}
else
	${VIRTUALENV} CI=1 nosetests -v --with-timer --timer-top-n 0 --with-coverage --cover-xml --cover-package=${PYTHON_MODULES} ${PYTHON_MODULES}
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

tdd:
	${VIRTUALENV} ls -d */ | \
		cut -d'/' -f1 | \
		egrep -v '$^${PYTHON_MODULES}$$' | \
		paste -s -d',' | \
		sed '/^$$/d;s/[[:blank:]]//g' | \
		xargs -e -I [] echo tdaemon --ignore-dirs=\"[]\" --custom-args=\"--with-notify --no-start-message\"

tox: ${REQUIREMENTS_TEST}
	${VIRTUALENV} tox

windows: ${PYINSTALLER} ${PYTHON_EXE} ${WINDOWS_BINARIES} ${TOOLS_PATH}/requirements.windows.check ${DOWNLOAD_PATH}/wxpython.installed
	@rm -rf dist/windows
	@mkdir -p dist/windows
	@wine ${PYTHON_EXE} ${PYINSTALLER} --onefile --windowed ${PYTHON_MODULES}.windows.spec --distpath dist/windows

dist/wednesday.zip: windows
	cd dist/windows && \
		zip -r wednesday.zip wednesday

dist: python_egg python_wheel dist/wednesday.zip


.PHONY: clean purge dist run windows
