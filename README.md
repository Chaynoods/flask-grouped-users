Prompt
---

Implement a REST service using a python web framework such as flask or django that can be used to store, fetch, and update user records. A user record can be represented in a JSON hash like so:

```json
{
    "first_name": "Joe",
    "last_name": "Smith",
    "userid": "jsmith",
    "groups": ["admins", "users"]
}
```

The service should provide the following endpoints and semantics:

```
GET /users/<userid>
    Returns the matching user record or 404 if none exist.
```

```
POST /users/<userid>
    Creates a new user record. The body of the request should be a valid user
    record. POSTs to an existing user should be treated as errors and flagged
    with the appropriate HTTP status code.
```

```
DELETE /users/<userid>
    Deletes a user record. Returns 404 if the user doesn't exist.
```

```
PUT /users/<userid>
    Updates an existing user record. The body of the request should be a valid
    user record. PUTs to a non-existant user should return a 404.
```

```
GET /groups/<group name>
    Returns a JSON list of userids containing the members of that group. Should
    return a 404 if the group doesn't exist or has no members.
```

```
POST /groups/<group name>
    Creates a empty group. POSTs to an existing group should be treated as
    errors and flagged with the appropriate HTTP status code.
```

```
PUT /groups/<group name>
    Updates the membership list for the group. The body of the request should 
    be a JSON list describing the group's members.
```

```
DELETE /groups/<group name>
    Removes all members from the named group. Should return a 404 for unknown 
    groups.
```


Install
---

Installation is simple: `bash install.sh` inside this folder.

This script will:

1. Check you have python 2 and virtualenv (installing virtualenv if not present)
2. Create a python virtual environment named "venv" in this folder
3. Install flask in said virtual environment.


Running the Server
---

To run the server, `./grouped_users/run_server.py` is all you need. The server will start on localhost, port 5000

If this fails, make sure that the `run_server.py` file is executable (`chmod a+x grouped_users/run_server.py`)


Running the Tests
---

To run the tests, `./grouped_users/run_tests.py` is all you need.

If this fails, make sure that the `run_tests.py` file is executable (`chmod a+x grouped_users/run_tests.py`)


Development Process
---

#### Research: 15 minutes
* Chose Flask over Django due to size of requested implementation
* Had never coded Flask before, so followed some [online "hello world"-esque tutorials](http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)

#### MVP of User resource: 1 hour
* Expand from tutorial-driven base into requested user model
* JSON-based error handling

#### Testing, round 1: 1 hour
* Sort out import issues to get hello world-esque test running and learn python's unittest
* Cover provided specification with controller-level tests, except for where behavior involved groups

#### Test-driving the Groups resource: 2 hours
* Two separate resources demanded factoring into two separate controllers, or flask "blueprints"
* Has-and-belongs-to-many relationship between users and groups demanded a join table ("memberships"), no controller needed
* Factor error handling out of individual controllers
* Add test cases to the UsersController test to cover posting up users with non-existant groups, and test cases for the GroupsController covering adding non-existant users to a given group

#### Clean-up: 45 minutes
* Write install script & this README
* Refactor code. Notice & strive for similarities across controllers, across DBM's, etc. leading to...

#### Next steps
* Noticed a lot of structural similarities between UsersController/UsersDBM and GroupsController/GroupsDBM, but wrestling with Flask to factor out shared code structure seems out of scope & unclear python would have the metaprogramming tools needed.
* Swap out in-memory DB for a real SQL (or at least SQLite) db. Consciously structured the in-memory DB very much like a real SQL db (tables as arrays of primitive values, using foreign keys / join tables instead of whole python objects where references are required) to make that transition simple & straightforward. Also factored the database managers (DBM's), controllers, models, and db object itself apart from each other to isolate & encapsulate persistence strategies.

#### Notes
* I haven't coded python in around 4 years, so I may have forgotten some of the pythonic ways of doing some things. Luckily, there was very little algorithmic work needed for this exercise: it was largely just straight-forward OOP factoring.
* I also haven't coded a web API in any professional context in 3 years, so my instincts for separation of concerns are largely based on memories of Rails & osmosis of working closely with backenders at my current job. It feels right to me (and has strong parallels with the client perspective of interacting with an API & storing the results to disk), and hopefully it is rather straight-forward to understand.

## Total: 6 hours