FROM python:3.8
        
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY . .

RUN pip install -r requirements.txt

# EXPOSE 8000

# CMD ["python3.8", "manage.py", "runserver", "0.0.0.0:8000"]

# sudo docker build -t <image_name>:<tag> .

# sudo docker run -p 8000:8000 <image_name>:<tag>
