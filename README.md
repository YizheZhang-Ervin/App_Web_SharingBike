# SharingBike  
## Run Django  
pip install -r requirements.txt  
cd SharingBike   
python manage.py runserver  
Browser: http://127.0.0.1:8000/  
  
## Commands  
pip freeze > requirements.txt  
  
## Start project  
django-admin startproject xxSite  
python manage.py startapp xxApp  
  
## Database  
python manage.py makemigrations xxApp  
python manage.py migrate  
python manage.py collectstatic  
  
## Backend Management  
python manage.py createsuperuser (name:ez,password:ez)  

# heroku deploy  
add gunicorn,django_heroku requirements  
heroku run python xxx  