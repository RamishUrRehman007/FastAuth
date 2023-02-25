# FastAuth
A microservice to authenticate &amp; authorize a user using FastAPI, PostgreSQL, SQLAlchemy &amp; Docker.

## Technologies
#### FastAPI
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

#### SQLAlchemy
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

#### PostgreSQL
PostgreSQL is an object relational database management system which is a system used for managing data in relations, or tables which are grouped into databases, so you can have multiple tables in one database.

#### Docker
Docker is a platform for developers to develop, deploy, and run applications with containers since containers are portable, lightweight and stackable.

## Project Description
FastAuth is a microservice to authenticate &amp; authorize a user. In this project, a POST request is being utilized to register a user, lets a user login and authenticate, a JWT and CSRF token is assigned, and then the user is authorized to GET details of itself. Technologies used in this project are FastAPI, PostgreSQL, SQLAlchemy &amp; Docker.

## Running the Application
1. Clone the respository into your local system
> git clone https://github.com/RamishUrRehman007/FastAuth.git

2. Run the following Docker Build commands to setup **Database with Migrations**
> docker-compose up -d postgres<br>
> docker-compose exec postgres sh -c '/mnt/migration.sh -d fast_auth'<br>

![DockerDatabase](images/docker_database.PNG)

3. Execute the following command to run Application in same **fastauth container**
> docker-compose up<br>

![DockerFastAuth](images/docker_fastauth.PNG)

3. Now, access to "http://localhost:10000/" on your browser to open swagger docs and test status endpoint.

![SwaggerStatusSuccess](images/swagger_status_success.PNG)

4. Lets perform operations using Swagger or Thunder Client!

> Register User<br>
![RegisterUser](images/register_user.PNG)

> User Authentication<br>
![LoginUser](images/login_user.PNG)

> Fetching User and Authorization<br>
![UserAuthorization](images/user_authorization.PNG)