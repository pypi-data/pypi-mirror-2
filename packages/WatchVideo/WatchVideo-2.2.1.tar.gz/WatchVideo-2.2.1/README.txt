.. -*- rst -*-

==========
WatchVideo
==========

:Project page: http://savannah.nongnu.org/projects/watchvideo
:Homepage: http://www.nongnu.org/watchvideo/
:License: GNU Affero General Public License v3+
:Version: 2.2.1

WatchVideo is an application to download or watch videos from many popular Flash
based sites using an external player or built-in VLC.

Requirements
============

For both GUI and CLI interface:

* Python 2.6, 2.7, 3.1 or later
* GetMediumURL 0.0a2 or later
* Distribute (``python-setuptools``)

The installation script will automatically install GetMediumURL if it
is not available.  It requires ``lxml`` which should be installed from
distribution package before (in Debian-based GNU/Linux distributions
it is named ``python-lxml``).

For GUI only:

* PyQt4 (``python-qt4``) or PySide
* VLC version 1.1 (optional, required for built-in player)
* ``python-notify`` (optional): uses the system's default mechanism to
  show notification messages
* FFmpeg (optional): needed for all operations related with video
  conversion, ripping or the built-in player.
* FFmpeg2theora (optional): needed to convert videos to Ogg Vorbis or
  Theora, but not for ripping audio

If you downloaded through Subversion:

* ``pyqt4-dev-tools`` (``pylupdate4``, ``pyrcc4``, ``pyuic4``)
* ``libqt4-dev`` (``lrelease``)
* Inkscape
* OptiPNG (optional)
* docutils

PyQt4 is used by default.  When it is not found, PySide is used but
there are known bugs when using it.  Set the environment variable
``WATCHVIDEO_QT`` to a space-separated sequence of package names tried to
use a different package (e.g. ``WATCHVIDEO_QT=PySide`` to use PySide on
systems where PyQt4 is installed).


Installation using ``easy_install``
===================================

.. note::

    This method doesn't install the desktop file nor the icon.
    
    Optional dependencies should be installed separately.

To install the newest version of WatchVideo using easy_install use the following command (as **root**):

``easy_install -U WatchVideo`` 



Installation from source
========================

Open a terminal in the extracted source folder and type ``sudo make install``.

These options (specified after ``make``) can be used to change the
installation directory:

  ``prefix``
    default is ``/usr/local``
  ``datarootdir``
    default is ``$prefix/share``

Unless the prefix is changed, root priviledges are needed for
installation.

To use different Python interpreter than the one found by the ``python``
command, specify it as the ``PYTHON`` variable.

You can instead call ``python setup.py install`` with options described
by ``python setup.py --help install`` and optionally install menu entry
and icon by ``make install-data``.

Installation of additional data (Optional)
======================================================
In case you don't have the **desktop file** and/or the **icon**, you can install them with the following command (as **root**):

``wget -O /usr/share/applications/watchvideo.desktop http://mirrors.fe.up.pt/pub/nongnu/watchvideo/watchvideo.desktop && wget -O /usr/share/pixmaps/watchvideo.svg http://mirrors.fe.up.pt/pub/nongnu/watchvideo/watchvideo.svg``

Using
=====

If installed
------------

If you installed the desktop file and icon there should be an entry in your menu under the Audio and Video section.


You can also call the app with the command::

  qtwatchvideo [OPTIONS] URL1 URL2 ...

or simply::

  qtwatchvideo

Run ``qtwatchvideo --help`` to see all options of the GUI version.

If you want to use the CLI version::

  watchvideo [OPTIONS] URL1 URL2 ...

Run ``watchvideo --help`` to see all options of the CLI version.

If not installed
----------------

.. note::

   If you downloaded through Subversion, first you need to do ``make``
   to generate the necessary files.

Running ``python setup.py develop --user`` with put scripts needed to
run WatchVideo in ``$HOME/.local/bin``, and use other file from the
directory where the source is located.  You might use the programs as
``~/.local/bin/qtwatchvideo`` and similarly ``watchvideo``, or write

::

  export PATH=$HOME/.local/bin:$PATH

before to use them like when installed.

Updating plugins
================

WatchVideo uses a package called GetMediumURL to get the information
from the video-sharing websites.  Some of these sites often change
their interfaces, when this happens it won't find the video.  In this case try to
update GetMediumURL, by doing the following in a terminal:
``easy_install -U GetMediumURL`` or using your distribution packages for
it.

Translating
===========

If you wish to translate this application, do the following:

1. Open a terminal in the source distribution directory.
2. Do ``make check-dependencies`` to see if you have the necessary
   dependencies.
3. Add a reference for your language to ``L10N`` in the Makefile.
4. Do ``make`` to generate the necessary files.
5. Translate the ``.ts`` file generated in the ``po``
   subdirectory. You can use Qt Linguist or any text editor of your
   choice.
6. When you're ready to test your translation, do ``make`` again.
