# jwt_authentication_fastapi
 JWT authenication in fastapi


## Description
This is a simple fastapi application that demonstrates how to use JWT for authentication. It has a simple user registration and login system. The user is authenticated using JWT and the token is used to access protected routes.



## Installation

### Clone the repository
```bash
git clone 'repository url'
cd jwt_authentication_fastapi
```
### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
### Install the requirements

```bash
pip install -r requirements.txt


```
### Run the application
```bash
uvicorn main:app --reload
```