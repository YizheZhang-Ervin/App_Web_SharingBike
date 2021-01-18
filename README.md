# SharingBike  
## User: First Time Run Django  
### Intall Dependency  
pip install -r requirements.txt  
   
### Database & static files  
cd SharingBike  
python manage.py collectstatic  
python manage.py makemigrations bikesys  
python manage.py migrate  
  
### Backend Management  
python manage.py createsuperuser(name:ez,password:ez)  
python manage.py runserver  
Browser: http://127.0.0.1:8000/  
  
## Developer: Coding  
### Developer Start New Project  
django-admin startproject xxSite  
python manage.py startapp xxApp  
  
### Developer Output Python Dependency
Virtual Env libs: pip freeze > requirements.txt  
Dependency libs: pipreqs ./  
  
### Developer heroku deploy  
add gunicorn requirements  
delete version nums  
heroku run python xxx  
  