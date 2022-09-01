# watering_plants__app_project

1. Installation instructions for the project:
   
   - Download project repository from Github.
   - Install Docker (https://docs.docker.com/get-docker/).
   - Create your virtualenv (and activate for project).
   - Launch project in Pycharm IDE.
   
2. SET UP PROJECT:
   Requirements:
   - python >= 3.10
   - django >= 4.0
   - postgres database
   - docker (commands to run server: docker-compose up (build))
   - set your EMAIL_HOST_USER, EMAIL_HOST_PASSWORD and DEFAULT_FROM_EMAIL (settings.py)
     # 'Less secure apps' option must be enabled in gmail for proper sending emails.
   - install requirements.txt (pip install -r requirements.txt)
   - python manage.py makemigrations, next: migrate
   - python manage.py loaddata initial_data-blog.json (if exists)
   - python manage.py createsuperuser
   - python manage.py runserver
   

!!!!
.env file and data from the docker-compose file removed from .gitignore and made available only for the project (to make it work).
