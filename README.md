# FastAuth

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlalchemy)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

FastAuth is a microservice designed to authenticate and authorize users through FastAPI, PostgreSQL, SQLAlchemy, and Docker. By utilizing modern standards like JWT (JSON Web Tokens) and CSRF (Cross-Site Request Forgery) tokens, FastAuth aims to secure accounts from common cyber threats such as token theft.

## Architecture

FastAuth leverages an architecture composed of Python, FastAPI, PostgreSQL, and Docker, with a significant emphasis on FastAPI middleware for authenticating JWT and CSRF tokens before accessing actual endpoints. This design ensures a secure and efficient authentication and authorization process.

## Technologies

- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+, based on standard Python type hints.
- **SQLAlchemy**: The Python SQL toolkit and Object Relational Mapper that provides application developers with the full power and flexibility of SQL.
- **PostgreSQL**: An object-relational database management system, known for its reliability and data integrity.
- **Docker**: A platform for developing, deploying, and running applications with containers, which are portable, lightweight, and stackable.

## Project Description

FastAuth is a microservice focused on user authentication and authorization. It uses a POST request for user registration, login, and authentication, assigning JWT and CSRF tokens to authorize users to access their details. The project utilizes FastAPI for the web framework, PostgreSQL for the database, SQLAlchemy for ORM, and Docker for containerization.

## Getting Started

To get FastAuth running on your local machine, follow these steps:


## Prerequisites

Before you begin, ensure you have installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/downloads)

## Setup and Installation

1. **Clone the Repository**

   Clone the FastAuth repository to your local machine:

   ```bash
   git clone https://github.com/RamishUrRehman007/FastAuth.git


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