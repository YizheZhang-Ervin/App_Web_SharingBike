# Sharing Bike System
## System Architecture
### Backend: Django Custom RESTful Framework  
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
  
## Project Design  
1. Customer Interface  
- Rent bikes
- Return bikes
- Report defective bikes
  
2. Operator Interface  
- Repair bikes
- Track all bikes
- Track defective bikes
  
3. Manager Interface  
- Data Visualization Report  
  
## Database Design
1. User
- user id (pk)
- balance
- class
- name
- password
  
2. Location
- location id (pk)
- description
  
3. Bike
- bike id (pk)
- location (fk)
- available status
- defective status
  
4. Record
- record id (pk)
- user id (fk)
- bike id (fk)
- begin time
- end time
- begin location
- end location
- finished flag
  
## Data Analysis
1. Compute different time different location quantity of bikes  
2. Compute the demand of bikes of different time different location  
3. Arrange bikes to move between locations in given time, including multiple locations bikes move to multiple locations  
4. Use dijskra to find shortest path for moving bikes  
5. Use shortest path first method to decide Order of movement  
6. Analysis: only analyze time period, not take consider in different days effect

## What's next?
1. database model: picture