#!/bin/bash

if [ "$ELASSANDRA_LOAD_CQLSHRC" = "true" ]; then
    export ELASSANDRA_LOGIN="$(awk '!/^#/ &&/username/ { print $3 }' /root/.cassandra/cqlshrc)"
    export ELASSANDRA_PASSWORD="$(awk '!/^#/ && /password/ { print $3 }' /root/.cassandra/cqlshrc)"
    export ELASSANDRA_CERTFILE="$(awk '!/^#/ && /certfile/ { print $3 }' /root/.cassandra/cqlshrc)"
fi


# specific to strapcloud environment
if [ -f "/etc/profile.d/docker-context.sh" ]; then
    source "/etc/profile.d/docker-context.sh"
fi
if [ -n "$ELASSANDRA_LOCAL_RPC" ] && [ -z "$ELASSANDRA_ENDPOINTS" ]; then
    export ELASSANDRA_ENDPOINTS="$ELASSANDRA_LOCAL_RPC"
fi

export PYTHONPATH="/"

if [ "$DEBUG" = "true" ]; then
    env
fi

python3 -m meetup.web