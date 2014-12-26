#!/bin/sh

cat >> /etc/rc.conf.local <<'EOF'
# See: conf/122477 for relevant discussion about this
_mdconfig_list="${_mdconfig_list} md99"
mdconfig_md99="-s $(cat /var/usr-tests.size.txt)M -t swap"
mdconfig_md99_cmd="tar -xJf /var/usr-tests.txz -C \${_mp} && mount -ru \${_mp}"
EOF
