# Bucketlist API

[![Build Status](https://travis-ci.org/Elbertbiggs360/buckelist-api.svg?branch=master)](https://travis-ci.org/Elbertbiggs360/buckelist-api)
[![Coverage Status](https://coveralls.io/repos/github/Elbertbiggs360/buckelist-api/badge.svg?branch=master)](https://coveralls.io/github/Elbertbiggs360/buckelist-api?branch=master)


This is a python application using SQLAlchemy and Flask 
to create a REST API backend to be used to compute commissions and float values
for agents of mobile money services

## Demo
You can request a demo from @elbertbiggs360 on twitter

You can also test the API demo hosted at https://burketlist.herokuapp.com in Postman

##Usage
| Endpoint                                    | Public Access |
| --------------------------------------------|:-------------:|
| POST /auth/login                            |    TRUE       |
| POST /auth/register                         |    TRUE       |
| POST /bucketlists/                          |    FALSE      |
| GET /bucketlists/                           |    FALSE      |
| GET /bucketlists/<id>                       |    FALSE      |
| PUT /bucketlists/<id>                       |    FALSE      |
| DELETE /bucketlists/<id>                    |    FALSE      |
| POST /bucketlists/<id>/items/               |    FALSE      |
| PUT /bucketlists/<id>/items/<item_id>       |    FALSE      |
| DELETE /bucketlists/<id>/items/<item_id>    |    FALSE      |

---

## Features
- Create bucketlist
- Create bucketlist entry item
- Edit entries
- Delete entries
- Delete Bucketlist

## Work done
Implemented API to do the following
* Create bucketlists
* Edit bucketlists
* Delete bucketlists

## Work left:
* Add support for token based authentication
* Create pagination support
* Create searching by name
* Support for load on multiple requests
* Build mobile front end for app with ionic
* Add unit tests

## Prerequisites:
* Python 3.3^
* Flask
* SQLAlchemy

## API Engine

#### How to run the engine
* Clone the application: *git clone https://github.com/Elbertbiggs360/buckelist-api.git*
* cd into the bucketlist-api: `cd bucketlist-api`
* Run `python install -r requirements.txt`
* The above command downloads all the dependencies needed for the project and starts the engine.
* Run the server `npm run`
* You can now access the api from . 
* Default creds: *Username*: user *Password*: password

---

## License
>You can check out the full license [here](https://github.com/Elbertbiggs360/buckelist-api/blob/master/LICENSE)

![MIT License](https://github.com/Elbertbiggs360/buckelist-api/blob/master/mit.png)
This project is licensed under the terms of the **MIT** license.