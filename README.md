# For Runnig the Project at your local

### Install virtualenv
> sudo apt install python3-virtualenv

<br>

### Create Virtual Environment by below command
> virtualenv venv

<br>

### Activate virtualenv
> source virtualenv/bin/activate

<br>

### Install All Requirements
> pip install -r requirements.txt


<br>

### Command For Running project
> python3 manage.py makemigrations

> python3 manage.py migrate

> python3 manage.py runserver

<br>

### For Testing the API 
Hit the postman collection given.

# or

### Run below command
> sudo docker compose up

### Go inside django_backend_assignment container and then execute makemigrations command and migrate command
> sudo docker exec -it django_backend_assignment bash

> python3.8 manage.py makemigrations

> python3.8 manage.py makemigrations accounts

> python3.8 manage.py makemigrations movies_collection

> python3.8 manage.py migrate 
