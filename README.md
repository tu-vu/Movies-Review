# Movies-Review

![Python](https://img.shields.io/badge/Python-v3.8.3-0087d8?logo=python&logoColor=white&style=flat-square)
![Flask](https://img.shields.io/badge/Flask-v1.1.2-a90606?logo=flask&logoColor=white&style=flat-square)
![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-v2.4.3-a90606?logo=flask&logoColor=white&style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v12.1-336791?logo=postgresql&logoColor=white&style=flat-square)
![Bootstrap](https://img.shields.io/badge/Bootstrap-v4-563D7C?logo=bootstrap&logoColor=white&style=flat-square)
![API](https://img.shields.io/badge/API-TMDB-01D277?logo=themoviedatabase&logoColor=white&style=flat-square)

![Demo1](demo1.png)
![Demo2](demo2.png)

Website found here: https://moviebia.herokuapp.com/  

You can use the following credentials if you don't want to sign up:  
- Email: demo_account@gmail.com  
- Password: 123456

## Installation
##### Installation via requirements.txt
    cd Movies-Review
    mkvirtualenv Movies-Review
    pip3 install -r requirements.txt
    flask run

## Usage
##### Create a .env file in project folder
##### Replace the following values with yours in .env file
* `FLASK_APP`: Entry point of the application(should be 'wsgi.py')
* `FLASK_ENV`: Enable/Disable development mode by setting it to development/production
* `SECRET_KEY`: Randomly generated string of characters used to encrypt your app's data.'
* `DATABASE_URL`: URI of a SQL database
* `API_KEY`: The API key can be accquired via [TMDB](https://developers.themoviedb.org/3/getting-started/introduction)
* `DEBUG`: Enable/Disable debug mode by setting it to True/False
* `TESTING`: Enable/Disable testing mode by setting it to True/False

## Collaborator
* [TenLaGi123](https://github.com/TenLaGi123)
