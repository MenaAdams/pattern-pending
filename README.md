# Pattern Pending 

[![Pattern Pending](/static/logo.png)](https://github.com/menaadams/pattern-pending)

## Summary
Pattern Pending is a Ravelry client that interfaces with Ravelry's API for users to easily browse knitting patterns and view user statistics in doughnut charts. I made Pattern Pending because I'm a knitter who loves to browse patterns but found Ravelry's interface unintuitive for that purpose. I wanted to highlight what makes Ravelry useful to me.


## Tech Stack
__Frontend:__ HTML5, CSS, ReactJS, Javascript, jQuery

__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy

__APIs:__ Ravelry


## Features

Pattern Pending gets and stores public Ravelry data about the user's projects, pattern library, and interests. 

![login](https://user-images.githubusercontent.com/27045372/59570235-ee81b100-9049-11e9-94a1-75e0bc20a31d.gif)


Users then enter a search criteria (yarn or item type).

![search](https://user-images.githubusercontent.com/27045372/59570236-ef1a4780-9049-11e9-830f-4d693262b336.gif)


Pattern Pending retrieves and displays search results using the Ravelry API.

![search-results](https://user-images.githubusercontent.com/27045372/59570237-ef1a4780-9049-11e9-84bb-7ba6e5460e5d.gif)


Pattern Pending also uses chart.js to create a fun representation of the user's project data.

![charts](https://user-images.githubusercontent.com/27045372/59570228-dd38a480-9049-11e9-9665-298a831f04ca.png)


## Setup/Installation 

#### Requirements:

- PostgreSQL
- Python 3.6
- Ravelry API key

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/MenaAdams/pattern-pending.git
```
Create a virtual environment🔮:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Get your own secret keys🔑 for [Ravelry](https://www.ravelry.com/pro/developer). Save them to a file `secrets.sh`. Your file should look something like this:
```
export RAVELRY_USERNAME='abc'
export RAVELRY_PASSWORD='abc'
```
Create database 'patterns'.
```
$ createdb patterns
```
Create your database tables.
```
$ python -i model.py
$ db.create_all()
$ add_categories_to_db()
```
Run the app from the command line.
```
$ python server.py
```

## TODO✨
* Add testing module
* Implement OAuth so users can log in using their Ravelry account
* Add Infinite Scroll to search results
* Add user recommendations module


## About the Developer
Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/menaadams/)