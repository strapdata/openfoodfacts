Demo
====

Connect to the cluster
```
ssh centos@104.214.238.168
ssh centos@40.114.238.211
ssh centos@40.114.238.193
```

Start the containers
```
docker stack deploy -c docker-compose-viz-prod.yml viz
docker stack deploy -c docker-compose-meetup-prod.yml meetup
```

Remove the container
```
docker stack rm meetup
```

Visit the application :
```
https://meetup.903403a9-617f-47ac-933e-537a73091e54.azure.strapcloud.com/
```

Swarm viz :
```
https://viz.903403a9-617f-47ac-933e-537a73091e54.azure.strapcloud.com
```