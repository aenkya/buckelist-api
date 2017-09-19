# Bucketlist API

[![Build Status](https://travis-ci.org/Elbertbiggs360/buckelist-api.svg?branch=master)](https://travis-ci.org/Elbertbiggs360/buckelist-api)
[![Coverage Status](https://coveralls.io/repos/github/Elbertbiggs360/buckelist-api/badge.svg?branch=master)](https://coveralls.io/github/Elbertbiggs360/buckelist-api?branch=master)
[![Code Climate](https://codeclimate.com/github/Elbertbiggs360/buckelist-api/badges/gpa.svg)](https://codeclimate.com/github/Elbertbiggs360/buckelist-api)
[![Issue Count](https://codeclimate.com/github/Elbertbiggs360/buckelist-api/badges/issue_count.svg)](https://codeclimate.com/github/Elbertbiggs360/buckelist-api)
![MIT License](https://github.com/Elbertbiggs360/buckelist-api/blob/master/mit.png)

This is a python application using SQLAlchemy and Flask 
to create a REST API backend to be used to compute commissions and float values
for agents of mobile money services

## Demo
You can request a demo from @elbertbiggs360 on twitter

You can also test the API demo hosted at https://buckelist-api.herokuapp.com in Postman

##Usage

| EndPoint | Functionality | Public Access |
| -------- | ------------- | ------------- |
| `POST /auth/login`| Logs a user in | TRUE |
| `POST /auth/register`| Register a user | TRUE |
| `POST /bucketlists/`| Create a new bucket list | FALSE |
| `GET /bucketlists/`| List all the created bucket lists | FALSE |
| `GET /users/`| List all the created users | FALSE |
| `GET /users/\<id>`| Get a specific user | FALSE |
| `GET /bucketlists/\<id>`| Get single bucket list | FALSE |
| `PUT /bucketlists/\<id>`| Update this bucket list | FALSE |
| `DELETE /bucketlists/\<id>`| Delete this single bucket list | FALSE |
| `POST /bucketlists/\<id>/items/`| Create a new item in bucket list | FALSE |
| `PUT /bucketlists/\<id>/items/<item_id>`| Update a bucket list item | FALSE |
| `DELETE /bucketlists/\<id>/items/<item_id>`| Delete an item in a bucket list | FALSE |
| `GET /bucketlists?limit=\<number>`| Gets a number of bucket lists relative to the value passed in number. Maximum records is 100 | FALSE |
| `GET /bucketlists?q=\<bucketlist_name>`| Search for bucket list with the same name as that passed in bucketlist_name | FALSE |

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |

---

## Features
- Signup and login User
- Create bucketlists
- Create items

## Work done
Implemented API to do the following
* Create bucketlists
* Edit bucketlists
* Delete bucketlists
* Token Based Authentication
* Register User
* Login User
* Create bucketlist items
* Edit items
* Delete bucketlist items
* Search
* Pagination

### Work left:
Build mobile front end for app with ionic

## Prerequisites:
* Python 3.3^
* Flask
* PostGres

## API Engine

#### How to run the engine
* Clone the application: *git clone https://github.com/Elbertbiggs360/buckelist-api.git*
* cd into the bucketlist-api: `cd buckelist-api`
* Run `python install -r requirements.txt`
* Initialize, migrate, and upgrade the database:
    ```
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```
* The above command downloads all the dependencies needed for the project
* Run the server `python run.py`
* You can now access the api from 127.0.0.1:5000/api/v1

---

## Sample Requests

To register a new user:
![User Registration](https://github.com/elbertbiggs360/buckelist-api/blob/master/assets/screenshots/register.png)

To create a bucketlist (includes the token in the header):
![User Login](https://github.com/elbertbiggs360/buckelist-api/blob/master/assets/screenshots/create_bucketlist.png)

To search for a bucketlist:
![Searching for a bucketlist](https://github.com/elbertbiggs360/buckelist-api/blob/master/assets/screenshots/search.png)

To update item:
![Updating an item](https://github.com/elbertbiggs360/buckelist-api/blob/master/assets/screenshots/update_item.png)

## Testing
- To test, run the following command: ```coverage run --source app run_tests.py```
- View the test coverage with: ``` coverage report ```

## License
>You can check out the full license [here](https://github.com/Elbertbiggs360/buckelist-api/blob/master/LICENSE)

This project is licensed under the terms of the **MIT** license.