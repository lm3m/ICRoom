#!/bin/bash
sudo docker stack rm icroom 
sudo docker build -t lm3m/icroom.0 .  
sudo docker stack deploy -c docker-compose.yml icroom
sleep 2s
WEB=$(sudo docker container ls -f "name=icroom_web.1" -q)  
sudo docker logs --follow $WEB
