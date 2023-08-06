# Copyright (C) 2010  Carlos Pais  <freemind@lavabit.com>
# Copyright (C) 2010  Michał Masłowski  <mtjm@mtjm.eu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# GNU-style variables for directories where the files will be
# installed.
prefix = /usr/local
datarootdir = $(prefix)/share

DEPENDENCIES = "lxml getmediumurl"

# Use this Python interpreter.  Should be Python 2.5, 2.6 or 2.7.
PYTHON = python

# Support both Debian's modified docutils script names and the
# upstream ones.
ifdef RST2HTML
else ifeq ($(shell which rst2html 2>/dev/null),)
RST2HTML=rst2html.py
else
RST2HTML=rst2html
endif

# Commands for installation of files.
INSTALL = install
INSTALL_DATA = $(INSTALL) -m 644

# HTML files made from ReST formated source.
DOCS = README.html

# Files generated from Qt4 user interfaces.
UIS = watchvideo/ui_about.py watchvideo/ui_add_videos.py \
	watchvideo/ui_main.py watchvideo/ui_preferences.py
# All generated Python modules.
GENERATED = $(UIS) \
	watchvideo/icons_rc.py watchvideo/translations_rc.py
# PNGs of various sizes generated from SVG.
MEDIA_PNGS = media/preferences.png media/quit.png \
	media/Web-browser.png \
	media/watchvideo-32x32.png \
	media/watchvideo-200x200.png
# These are used in icons, not in the program.
ICON_PNGS = media/watchvideo-48x48.png
# Language codes of all translations.
L10N = cs es pl pt
# All Python modules where translatable strings are found.
SRC = $(UIS) \
	$(shell ls watchvideo/*.py | grep -v watchvideo/translations_rc.py)
# All graphics to be included in the icons.qrc resource.
MEDIAS = media/pause.png media/dialog-ok-apply.png \
	media/edit-clear-history.png media/edit-clear-list.png \
	media/edit-copy.png media/error.png media/folder-open.png \
	media/harddisk-add.png media/history.png media/internet-download.png \
	media/internet-play.png media/klipper.png media/list-add.svg \
	media/list-remove.png \
	media/refresh.png media/start.png media/stop.png \
	media/view-history.png \
	media/high-quality.png media/normal-quality.png \
	media/search.png\
	$(MEDIA_PNGS)
# All modules used for tests.  Not including all names here, since
# there won't be generated Python modules in that directory.
TESTS := $(shell find tests_watchvideo -name '*.py')

# egrep regular expression for names of files which are generated or
# copied from other projects and should not be checked by pyflakes and
# similar tools.
GENERATED_REGEX = '^watchvideo/(ui_.*|.*_rc|vlc)\.py$$'

# These don't need changes.

TS_FILES := $(L10N:%=po/%.ts)
QM_FILES := $(L10N:%=po/%.qm)
QRC_FILES = src_ui/icons.qrc src_ui/translations.qrc

SHELL = /bin/sh

all: $(GENERATED) $(ICON_PNGS) $(DOCS)

clean:
	find . -name "*.pyc" -delete 2>/dev/null
	find . -name "*~"    -delete 2>/dev/null

# Remove files which are generated using special tools and are
# included in the distribution.
maintainer-clean:
	-rm -f $(GENERATED) $(QRC_FILES) $(MEDIA_PNGS) $(ICON_PNGS)

install: all installdirs install-data
	for d in $(DEPENDENCIES); \
	do easy_install -U $$d; done
	$(PYTHON) setup.py install --prefix=$(prefix)

# Might be useful in packaging scripts calling setup.py with other
# arguments than in the above rule.
install-data: installdirs
	$(INSTALL_DATA) media/watchvideo.svg \
		$(DESTDIR)$(datarootdir)/pixmaps/watchvideo.svg
	$(INSTALL_DATA) watchvideo.desktop \
		$(DESTDIR)$(datarootdir)/applications/watchvideo.desktop

# Make directories needed for install.
installdirs:
	mkdir -p $(DESTDIR)$(prefix)
	mkdir -p ${DESTDIR}$(datarootdir)/pixmaps
	mkdir -p ${DESTDIR}$(datarootdir)/applications

uninstall:
	rm -rf $(DESTDIR)$(prefix)/lib/python2.6/dist-packages/watchvideo*
	rm -f $(DESTDIR)$(prefix)/bin/watchvideo_*
	rm -f $(DESTDIR)$(datarootdir)/applications/watchvideo*
	rm -f $(DESTDIR)$(datarootdir)/pixmaps/watchvideo*

MANIFEST.in: Makefile
	@echo '  'GEN'       ' $@
	@echo include src_ui/translations.qrc > $@
	@echo include src_ui/icons.qrc >> $@
	@for f in $(L10N:%=po/%.qm) $(MEDIA_PNGS) $(ICON_PNGS) $(DOCS) ; \
	do echo include $$f >> $@ ; done

dist: all MANIFEST.in
	$(PYTHON) setup.py sdist --dist-dir=. --formats=gztar

media/watchvideo-%.png: media/watchvideo.svg Makefile
	@echo '  'INKSCAPE'  ' $@
	@inkscape -e $@ -w $(shell echo $* | sed 's/x.\+//') \
		-h $(shell echo $* | sed 's/.\+x//') $< > /dev/null 2>&1
	@echo '  'OPTIPNG'   ' $@
	@-optipng -quiet $@

media/preferences.png: media/preferences.svg Makefile
	@echo '  'INKSCAPE'  ' $@
	@inkscape -e $@ -w 32 -h 32 $< > /dev/null 2>&1
	@echo '  'OPTIPNG'   ' $@
	@-optipng -quiet $@

media/quit.png: media/quit.svg Makefile
	@echo '  'INKSCAPE'  ' $@
	@inkscape -e $@ -w 32 -h 32 $< > /dev/null 2>&1
	@echo '  'OPTIPNG'   ' $@
	@-optipng -quiet $@

media/%.png: media/%.svg Makefile
	@echo '  'INKSCAPE'  ' $@
	@inkscape -e $@ -w 128 -h 128 $< > /dev/null 2>&1
	@echo '  'OPTIPNG'   ' $@
	@-optipng -quiet $@

watchvideo/ui_%.py: src_ui/ui_%.ui Makefile
	@echo '  'PYUIC4'    ' $@
	@pyuic4 $< | sed \
		-e 's/from PyQt4/from watchvideo.qt/' \
		-e 's/import icons_rc/from watchvideo import icons_rc/' \
		-e '/import icons_rc/aassert icons_rc' > $@

watchvideo/%_rc.py: src_ui/%.qrc Makefile
	@echo '  'PYRCC4'    ' $@
	@pyrcc4 -o - $< | sed 's/from PyQt4/from watchvideo.qt/' > $@

watchvideo/icons_rc.py: $(MEDIAS)

%.ts: $(SRC) Makefile
	@echo '  'PYLUPDATE4 $@
	@pylupdate4 $(SRC) -ts $@
	@sed -i 's,<location filename="\([^"]\+\)" line="[0-9]\+"/>,<location filename="\1"/>,' $@

%.qm: %.ts Makefile
	@echo '  'LRELEASE'  ' $@
	@lrelease $< -qm $@

watchvideo/translations_rc.py: $(L10N:%=po/%.qm)

src_ui/icons.qrc: $(MEDIAS) Makefile
	@echo '  'GEN'       ' $@
	@echo '<RCC><qresource>' > $@
	@for resource in $(MEDIAS) ; \
	do echo '<file>../'$$resource'</file>' >> $@ ; done
	@echo '</qresource></RCC>' >> $@

src_ui/translations.qrc: Makefile
	@echo '  'GEN'       ' $@
	@echo '<RCC><qresource>' > $@
	@for language in $(L10N) ; \
	do echo '<file>../po/'$$language'.qm</file>' >> $@ ; done
	@echo '</qresource></RCC>' >> $@

check-dependencies:
	@PYTHON=$(PYTHON) $(SHELL) ./utils/check-dependencies.sh

pyflakes: $(ALL_SRCS)
	@-pyflakes $$(ls watchvideo/*.py | egrep -v $(GENERATED_REGEX))


pylint: $(ALL_SRCS)
	@-pylint \
		--output-format=colorized \
		--include-ids=y \
		--report=n \
		--disable=C0103 \
		--disable=C0111 \
		--disable=C0301 \
		--disable=C0321 \
		--disable=W0614 \
		$$(ls watchvideo/*.py | egrep -v $(GENERATED_REGEX))

pylint-tests: $(TESTS)
	@-pylint \
		--output-format=colorized \
		--include-ids=y \
		--report=n \
		--generated-members=resource_filename \
		--good-names=setUp,tearDown \
		$(TESTS)

pep8: $(ALL_SRCS) $(TESTS)
	@-pep8 watchvideo tests_watchvideo

style: pyflakes pylint pylint-tests pep8

check: $(SRCS) $(TESTS) Makefile
	PYTHONPATH=.:$$PYTHONPATH \
		coverage run --source=watchvideo --branch \
			tests_watchvideo/__init__.py
	coverage html --omit=$$(ls watchvideo/*.py \
		| egrep $(GENERATED_REGEX) | tr \\n ,)

%.html: %.txt Makefile
	${RST2HTML} $< $@

.PHONY: all clean maintainer-clean install installdirs uninstall dist \
	check-dependencies pyflakes pylint pylint-tests pep8 style check

.SECONDARY: $(TS_FILES)
