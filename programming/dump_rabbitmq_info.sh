#!/bin/sh

while :
do
	set -x
	rabbitmqctl list_exchanges $* name type durable
	rabbitmqctl list_queues $* name messages durable
	rabbitmqctl list_bindings $* source_name source_kind destination_name destination_kind routing_key
	set +x
	sleep 10
	clear
done
