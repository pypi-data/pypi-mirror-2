#!/bin/bash

if [ "$1" = "" ]; then
	echo "Pleas pass a .svg file to convert"
	exit 1
fi

for i in 14 64 192;
	do rsvg -f png -w$i -h$i $1 $i.png
done
