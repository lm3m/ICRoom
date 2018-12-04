# ICRoom

Should be able to be deployed with docker.

Currently the docker-compose.yml uses a tag called: lm3m/icroom.0

The deploy.sh script is the one used during development, which should setup the app and a redis instance to go with it, along with the networking and volumes it would need.

General layout of the code:
toplevel - requirements, docker files, etc.
ICRoom - main app, and helpers (including the swagger infrastructure)
ICRoom\controllers - the controllers for the various routes
ICRoom\models - the models for each of the data types
todo.md - list of things I would fix next

once the app is up and running the routes are up at:
<host>:4000/api
the swagger which goes over the details of the API are at:
http://<host>:4000/api/

**API Details
user creation:
	POST /api/users/ 
	with a body of:
	{
		"username" : "test",
		"password": "test"
	}

user login:
	PATCH /api/users/test?action=login 
	{
		"password": "test"
	}
returns:
	{
		"auth_token": "<token>"
	}

topic creation:
	POST /api/topics/ 
	header:
		authorization: Bearer <auth_token>
	with a body of:
	{
 		"title": "unique title",
  		"description": "topic description"
	}
returns:
	topic_id

topic list:
	GET /api/topics/
	header:
		authorization: Bearer <auth_token>
returns
[
	{
		"id": "topic_id",
		"title": "title",
		"description": "description"
	}, ...
]

message creation:
	POST /api/messages/
	{
 		"message_body": "Message",
  		"topic_id": "topic_id",
  		"parent_id" : "parent_id, if this message is a reply to another message"
	}
	header:
		authorization: Bearer <auth_token>
returns:
	message_id

message list:
	GET /api/messages/ HTTP/1.1
	header:
		authorization: Bearer <auth_token>
returns
[
	{
		"id": "message_id",
		"topic_id": "topic_id",
		"creator_id": "user_id",
		"message_body": "message",
		{"parent_id" : "optional parent_id"}
	},
]
