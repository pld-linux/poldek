#!/bin/sh
#
# poldek-config - poldek(1) configuration program
#
# poldek-config is an program to provide consistent configurability.
# It accesses the main configuration file /etc/poldek/poldek.conf(5)
# in a manner that is easy to use by scripted applications.
#
# Author: Elan Ruusamäe <glen@pld-linux.org>
# Date: 2015-11-13

usage() {
	cat <<EOF
Usage: $0 [options] command

Commands:

ignore [PACKAGE] [PACKAGE...]
    Ignore package list - packages fits given mask will be invisible.

hold [PACKAGE] [PACKAGE...]
    Prevent package listed from being upgraded if they are already installed.

keep_downloads yes|no
    Do not remove downloaded packages after its successful installation.

cachedir /var/cache/poldek
    Cache directory for downloaded files. NOTE that parent directory of cachedir must exist.

EOF
}

die() {
	echo >&2 "$PROGRAM: $*"
	exit 1
}

option_set() {
	local option="$1"; shift
	sed -i -re "/^#?$option\s*=/ s#.*#$option = $*#" "$poldek_conf"
}

# parse command line args
parse_arguments() {
	t=$(getopt -o h --long help -n "$PROGRAM" -- "$@")
	[ $? != 0 ] && exit $?
	eval set -- "$t"

	while :; do
		case "$1" in
		-h|--help)
			usage
			exit 0
		;;
		--)
			shift
			break
		;;
		*)
			die "Internal error: [$1] not recognized!"
		;;
		esac
		shift
	done

	if [ $# = 0 ]; then
		usage
		exit 1
	fi

	command=$1; shift
	arguments="$*"
}

main() {
	parse_arguments "$@"

	case "$command" in
		ignore|hold)
			option_set "$command" "$arguments"
			;;
		keep_downloads)
			option_set "keep downloads" "$arguments"
			;;
		cachedir|cache_dir)
			option_set "cachedir" "$arguments"
			;;
		*)
			die "Unknown command: $command"
			;;
	esac
}

PROGRAM="${0##*/}"
poldek_conf=/etc/poldek/poldek.conf

main "$@"
