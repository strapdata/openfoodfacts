CREATE KEYSPACE IF NOT EXISTS "_kibana" WITH replication = {'class': 'NetworkTopologyStrategy','DC1':'1'};
CREATE ROLE kibana WITH PASSWORD = 'kibana' AND LOGIN = true;
INSERT INTO elastic_admin.privileges (role,actions,indices) VALUES ('kibana','cluster:monitor/.*','.*');
GRANT CREATE ON KEYSPACE "_kibana" TO kibana;
GRANT ALTER ON KEYSPACE "_kibana" TO kibana;
GRANT SELECT ON KEYSPACE "_kibana" TO kibana;
GRANT MODIFY ON KEYSPACE "_kibana" TO kibana;
GRANT SELECT ON KEYSPACE meetup TO kibana;