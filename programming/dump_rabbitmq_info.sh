#!/bin/sh

while :
do
	rabbitmqctl list_exchanges $*
	rabbitmqctl list_queues $*
	set -x
	rabbitmqctl list_bindings $* source_name source_kind destination_name destination_kind routing_key
	set +x
	sleep 10
	clear
done
