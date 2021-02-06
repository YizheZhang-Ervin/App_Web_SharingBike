# SharingBike  

## Features
Customer: Rent Bike + Return Bike + Report for Repairing Bike  
Operator: Repair Bike + Track Bike Locations + Balance Different Location Bike Quantities  
Manager: Data Report  
  
## Infrastructure
Frontend: Antd + React + Axios + Echarts  
Backend: Django RESTful + Sqlite  
  
## Run
cd frontend > npm install  
npm run build  
move frontend/static folder to backend/static  
workon env_develop  or source ./activate  
cd backend > pip install -r requirements.txt  
python manage.py runserver  
  
## FrontEnd: React
### start project  
create-react-app xxApp  
  
### modules  
npm install antd --save  
npm install axios --save  
npm install --save react-router-dom  
npm install @ant-design/icons  
  
### other commands  
npm start  
npm test  
npm run build  
npm run eject  
  
## BackEnd: Django
### start project  
django-admin startproject xxSite  
python manage.py startapp xxApp  
  
### Libs
pip install django  
pip install djangorestframework  
pip install django-cors-headers   
  
### Database & static files  
cd SharingBike  
python manage.py collectstatic  
python manage.py makemigrations
python manage.py migrate  
  
### Backend Management  
python manage.py createsuperuser(name:ez,password:ez)  
python manage.py runserver  
Browser: http://127.0.0.1:8000/  
  
### Dependency List  
Virtual Env libs: pip freeze > requirements.txt   
Dependency libs: pipreqs ./  
pip install -r requirements.txt   
  
## Heroku Deploy  
add gunicorn requirements  
delete version nums  
heroku run python xxx  
  