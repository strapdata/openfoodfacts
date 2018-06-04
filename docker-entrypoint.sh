#!/bin/bash

if [ "$DEBUG" = "true" ]; then
    set -x
fi

if [ "$ELASSANDRA_LOAD_CQLSHRC" = "true" ]; then
    export ELASSANDRA_LOGIN="$(awk '!/^#/ &&/username/ { print $3 }' /root/.cassandra/cqlshrc)"
    export ELASSANDRA_PASSWORD="$(awk '!/^#/ && /password/ { print $3 }' /root/.cassandra/cqlshrc)"
fi

# specific to strapcloud environment
if [ -f "/etc/profile.d/docker-context.sh" ]; then
    source "/etc/profile.d/docker-context.sh"
fi
if [ -n "$LOCAL_ELASSANDRA_RPC" ] && [ -z "$ELASSANDRA_ENDPOINTS" ]; then
    export ELASSANDRA_ENDPOINTS="$LOCAL_ELASSANDRA_RPC"
fi

export PYTHONPATH="/"

if [ "$DEBUG" = "true" ]; then
    env
fi

exec python3 -u -m $PYTHON_MODULE