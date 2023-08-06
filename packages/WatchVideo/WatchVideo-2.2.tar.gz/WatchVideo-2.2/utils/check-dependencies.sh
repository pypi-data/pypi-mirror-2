#!/bin/sh

# Check if a program can be used.  Arguments: command name,
# package name, required or optional, what to do if missing.
check_cmd() {
    if which $1 > /dev/null 2>&1
    then
        echo "$2 ($3) - OK"
    else
        echo "$2 ($3) - Missing! $4"
    fi
}

# Check if a Python module can be used.  Arguments: module name,
# package name, required or optional, what to do if missing.
check_module() {
    if $PYTHON -c 'import '$1 2> /dev/null
    then
        echo "$2 ($3) - OK"
    else
        echo "$2 ($3) - Missing! $4"
    fi
}

# Like above, but don't write about it unless it is missing.
check_module_quiet() {
    if $PYTHON -c 'import '$1 2> /dev/null
    then
        echo "$2 ($3) - OK"
    else
        echo "$2 ($3) - Missing! $4"
    fi
}

echo "<---- Common dependencies ---->"
if which $PYTHON > /dev/null 2>&1
then
	vernum1=`$PYTHON -c 'import sys ; print(sys.version_info[0])'`
	vernum2=`$PYTHON -c 'import sys ; print(sys.version_info[1])'`

	#if version is 3.0 or later
	if [ $vernum1 -eq 3 ]
        then
		echo "WARNING: WatchVideo doesn't work with Python 3.x versions."
		echo "Please use Python 2.5, 2.6 or 2.7 (newer is better)."
	else
		echo "Python (required) - OK"
	fi
else
	echo "Python (required) - Missing!"
fi

check_module getmediumurl GetMediumURL required '(use make install)'
check_module lxml lxml required '(use make install)'

if $PYTHON -c 'try:
    import json
except ImportError:
    import simplejson
' 2> /dev/null
then
    echo 'json (optional) - OK'
else
    echo 'json (optional) - Missing!'
    echo 'The Dailymotion plugin needs json or simplejson,'
    echo 'update Python to 2.6 or 2.7 or install simplejson.'
fi

echo
echo "<---- GUI only  ---->"

if $PYTHON -c 'import PyQt4' 2> /dev/null
then
	echo "PyQt4 (required) - OK"
        # Some distributions allow installing Qt and PyQt4 without
        # some modules, so check each used one separately.
        check_module_quiet PyQt4.QtCore PyQt4.QtCore required
        check_module_quiet PyQt4.QtGui PyQt4.QtGui required
        check_module_quiet PyQt4.QtSvg PyQt4.QtSvg required
else
	echo "PyQt4 (required) - Missing!"
fi

check_module_quiet watchvideo.vlc libVLC "required for built-in player"
check_cmd vlc VLC "Required by libVLC"
check_cmd ffmpeg FFmpeg "Required for the built-in player and all the video/audio operations"
check_cmd ffmpeg2theora FFmpeg2theora optional
check_module pynotify pynotify optional

echo
echo "<----- Install dependencies ----->"

check_module setuptools setuptools required

echo
echo "<----- If you got a copy from Subversion ----->"

check_cmd pylupdate4 "PyQt4 development tools" pyqt4-dev-tools
check_cmd lrelease "Qt4 development tools" libqt4-dev
