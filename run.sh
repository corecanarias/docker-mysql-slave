#!/bin/bash

SLAVE_ID=${SLAVE_ID:-2}

if [ ! -f /etc/mysql/conf.d/slave.cnf ]; then
   cat > /etc/mysql/conf.d/slave.cnf <<EOL
[mysqld]
bind-address      = 0.0.0.0
server-id     = $SLAVE_ID
EOL
if


exec mysqld_safe
