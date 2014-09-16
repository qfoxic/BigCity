#!/bin/bash
HOST=127.0.0.1:8000
USER=vpaslav
PASS=123456

# -------------GROUPS
echo group-list
curl -X GET --user $USER:$PASS $HOST/group/
echo
echo group-data
curl -X GET --user $USER:$PASS $HOST/group/1/
echo
echo create-group
curl -X POST -H "Content-Type: application/json" --user $USER:$PASS -d '{"name": "group77777"}' $HOST/group/
echo
echo update-group
curl -X PUT -H "Content-Type: application/json" --user $USER:$PASS -d '{"name": "group88888"}' $HOST/group/2/
echo
echo delete-group
curl -X DELETE -H "Content-Type: application/json" --user $USER:$PASS $HOST/group/2/
echo
# -------------USER
echo user-list
curl -X GET --user $USER:$PASS $HOST/user/
echo
echo user-data
curl -X GET --user $USER:$PASS $HOST/user/1/
echo
echo create-user
curl -X POST \
 -H "Content-Type: application/json" --user $USER:$PASS \
 -d '{"username": "test777","email": "wowowow@uuu.uuu","first_name": "f","last_name": "l","is_active": true, "password": 123456}' $HOST/user/
echo
echo update-user
curl -X PUT -H "Content-Type: application/json" --user $USER:$PASS -d '{"email": "vvv@jjj.nnn"}' $HOST/user/2/
echo
echo delete-user
curl -X DELETE -H "Content-Type: application/json" --user $USER:$PASS $HOST/user/2/
echo
echo user-chpassword
curl -X POST -H "Content-Type: application/json" -d'{"password": 123456, "id": 1}' --user $USER:$PASS $HOST/user/1/chpasswd/
echo
echo user-addgroup
curl -X POST -H "Content-Type: application/json" -d'{"gid": 1}' --user $USER:$PASS $HOST/user/1/addgroup/
echo
echo user-rmgroup
curl -X POST -H "Content-Type: application/json" -d'{"gid": 1}' --user $USER:$PASS $HOST/user/1/rmgroup/
echo
echo user-groups
curl -X GET -H "Content-Type: application/json" --user $USER:$PASS $HOST/user/1/groups/
echo

