#!/bin/bash

usage()
{
cat << EOF
usage: $0 -u USERNAME -p PASSWORD -t TRANSLATE_ID

This script downloads translations from Notabenoid in the specified format.

OPTIONS:
	-h | --help	Show this message
	-u | --username	Notabenoid username
	-p | --password	Notabenoid password
	-t | --translateid	Notabenoid translate id
	-f | --format	Output format (txt,epub,fb2), default: txt
	-v | --verbose	Verbose
EOF
}

download_translate(){
	python3 notabenoid.py $USERNAME $PASSWORD $TRANSLATEID > $TRANSLATEID.txt
}

while :
do
	case $1 in
		-h | --help | -\?)
			usage
			exit 0
			;;
		-u | --username)
			USERNAME=$2
			shift 2
			;;
		-p | --password)
			PASSWORD=$2
			shift 2
			;;
		-t | --translateid)
			TRANSLATEID=$2
			shift 2
			;;
		-f | --format)
			FORMAT=$2
			shift 2
			;;
		-v | --verbose)
			VERBOSE="yes"
			shift
			;;
		--)
			shift
			break
			;;
		-*)
			printf >&2 'Option is not exist: %s\n' "$1"
			shift
			;;
		*)
			break
			;;
	esac
done

if [[ -z $USERNAME ]] || [[ -z $PASSWORD ]] || [[ -z $TRANSLATEID ]] ; then
	usage
	exit 1
fi

#set -x

# Save as *.txt by default
if [[ -z $FORMAT ]] ; then
	download_translate
else
	case $FORMAT in
		EPUB|epub)
			download_translate
			pandoc -s $TRANSLATEID.txt -t epub -o $TRANSLATEID.epub
			rm $TRANSLATEID.txt
			;;
		FB2|fb2)
			download_translate
			pandoc -s $TRANSLATEID.txt -t fb2 -o $TRANSLATEID.fb2
			rm $TRANSLATEID.txt
			;;
		*) ;;
	esac
fi

