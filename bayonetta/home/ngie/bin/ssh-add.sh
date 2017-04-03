#!/bin/sh

set +ae
eval `ssh-agent`
ssh-add
ssh-add ~/.ssh/id_rsa_FreeBSD
