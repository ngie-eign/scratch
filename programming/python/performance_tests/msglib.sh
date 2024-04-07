#!/bin/sh

_msg()
{
	local levelname=$1; shift

	echo "${0##/*}: $levelname: $@"
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
