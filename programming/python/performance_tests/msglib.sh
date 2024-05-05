#!/bin/sh


_SCRIPTNAME="$(basename "$0")"

_msg()
{
	local levelname=$1; shift

	echo "$_SCRIPTNAME: $levelname: $@"
}

debug()
{
	_msg "DEBUG" $@
}

error()
{
	_msg "ERROR" $@
}

info()
{
	_msg "INFO" $@
}

warning()
{
	_msg "INFO" $@
}
