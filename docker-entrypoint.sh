#!/bin/sh

. /etc/profile.d/docker-context.sh

export LOCAL_ELASSANDRA_LOGIN="$(awk '!/^#/ &&/username/ { print $3 }' /root/.cassandra/cqlshrc)"
export LOCAL_ELASSANDRA_PASSWORD="$(awk '!/^#/ && /password/ { print $3 }' /root/.cassandra/cqlshrc)"
export LOCAL_ELASSANDRA_CERTFILE="$(awk '!/^#/ && /certfile/ { print $3 }' /root/.cassandra/cqlshrc)"
export DEBUG=true

env

# replace elassandra variables in database connection settings
sed -i "s/LOCAL_ELASSANDRA_RPC/$LOCAL_ELASSANDRA_RPC/g" /meetup/database.py
sed -i "s/LOCAL_ELASSANDRA_LOGIN/$LOCAL_ELASSANDRA_LOGIN/g" /meetup/database.py
sed -i "s/LOCAL_ELASSANDRA_PASSWORD/$LOCAL_ELASSANDRA_PASSWORD/g" /meetup/database.py
sed -i "s:LOCAL_ELASSANDRA_CERTFILE:$LOCAL_ELASSANDRA_CERTFILE:g" /meetup/database.py

export PYTHONPATH="/"
python3 -m meetup.web