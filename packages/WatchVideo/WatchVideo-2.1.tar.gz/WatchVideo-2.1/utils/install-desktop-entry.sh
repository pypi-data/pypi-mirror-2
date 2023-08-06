#!/bin/sh

cd $(dirname $0)

if [ $# -eq 1 ]
then
	prefix=$1
else
    echo "-----------------------------------------------------------------------"
    echo "Since you didn't provide any prefix location, the prefix will be '/usr'"
	echo
	echo "Is that Ok? [y/n]"
	read answer

	if [ $answer != "y" ] && [  $answer != "yes" ]
	then
		exit 1
	fi
	
	prefix="/usr"
fi

echo "Copied files will go to:"
echo "$prefix/share/pixmaps/"
echo "$prefix/share/applications"
echo "---------------------------------------------------------------"

install -D ../media/watchvideo.svg \
	$prefix/share/pixmaps/watchvideo.svg
install -D ../watchvideo.desktop $prefix/share/applications

