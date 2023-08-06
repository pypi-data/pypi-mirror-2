DESTDIR="/"

EXAMPLES=echobot.py send_message_client.py  simple_send_message.py check_version.py roster.py
PY2_EXAMPLES=$(addprefix examples/,$(EXAMPLES))
PY3_EXAMPLES=$(addprefix py3-examples/,$(EXAMPLES))

PY2TO3=2to3-3.2

.PHONY: all build test version dist install
.PHONY: py3-all py3-build py3-test py3-install
.PHONY: update-doc doc pylint.log pylint ChangeLog www publish

all: build test

py3-all: py3-build

build: version
	umask 022 ; python setup.py build
	-cd examples && rm -f pyxmpp2 2>/dev/null && ln -s ../build/lib*/pyxmpp2 .
	-cd examples && chmod a+x *.py
	-cd tests && rm -f pyxmpp2 2>/dev/null && ln -s ../build/lib*/pyxmpp2 .
	-cd tests && chmod a+x *.py

py3-build: version $(PY3_EXAMPLES)
	umask 022 ; python3 setup.py build --build-base=py3-build
	-cd py3-examples && rm -f pyxmpp2 2>/dev/null && ln -s ../py3-build/lib*/pyxmpp2 .

py3-examples: $(PY3_EXAMPLES)

py3-examples/%.py: examples/%.py
	install -d py3-examples
	cp $< $@
	$(PY2TO3) --no-diffs -w -n $@
	sed -i -e's/^\(#!.*python\)/\13/' $@

test:
	$(MAKE) -C tests tests

doc:
	$(MAKE) -C doc

update-doc:
	$(MAKE) -C doc update-doc

pylint:	pylint.log

pylint.log: build
	./auxtools/pylint.sh $(CHECK_MODULE) | tee pylint.log

ChangeLog: 
	test -d .git && make cl-stamp || :
	
cl-stamp: .git
	git log > ChangeLog
	touch cl-stamp

version:
	python setup.py make_version

dist: build ChangeLog update-doc py3-examples
	-rm -f MANIFEST
	python setup.py sdist

clean:
	-python setup.py clean --all
	-[ -d py3-build ] && python3 setup.py clean --all --build-base=py3-build
	-rm -rf build/*

install: all
	umask 022 ; python setup.py install --root $(DESTDIR)

py3-install:
	umask 022 ; python3 setup.py build --build-base=py3-build install --root=$(DESTDIR)
