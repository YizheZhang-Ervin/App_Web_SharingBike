# Sharing Bike System
## System Architecture
### Backend: Django
1. Run Django Locally 
```  
pip install -r requirements.txt  
cd SharingBike   
python manage.py runserver  
Browser: http://127.0.0.1:8000/  
```  
  
2. Python Commands  
```  
pip freeze > requirements.txt  
```  
  
3. Django Start project  
```  
django-admin startproject xxSite  
python manage.py startapp xxApp  
```  
  
4. Django Database Process  
```  
python manage.py makemigrations xxApp  
python manage.py migrate  
python manage.py collectstatic  
```  
    
5. Django Backend Management  
```  
python manage.py createsuperuser (name:ez,password:ez)  
```  
  
6. heroku deploy  
```  
add gunicorn,django_heroku requirements  
heroku run python xxx  
```  
  
---  
    
### FrontEnd: HTML/CSS/JS/AXIOS  
  