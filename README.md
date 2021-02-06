# SharingBike  
## Infrastructure
frontend: Antd + React + Axios + Echarts    
backend: Django RESTful + Sqlite  

# Run
cd frontend > npm run build  
move static folder to backend/static  
cd backend > python manage.py runserver  
  
## React
npm install antd --save  
npm install axios --save  
npm install --save react-router-dom  
npm install @ant-design/icons  
create-react-app xxApp  
npm start  
npm test  
npm run build  
npm run eject  

## Django
### Developer Start New Project  
django-admin startproject xxSite  
python manage.py startapp xxApp  

### Database & static files  
cd SharingBike  
python manage.py collectstatic  
python manage.py makemigrations bikesys  
python manage.py migrate  
  
### Backend Management  
python manage.py createsuperuser(name:ez,password:ez)  
python manage.py runserver  
Browser: http://127.0.0.1:8000/ 

### Requirements  
Virtual Env libs: pip freeze > requirements.txt  
Dependency libs: pipreqs ./  
pip install -r requirements.txt  
   
## Heroku Deploy  
add gunicorn requirements  
delete version nums  
heroku run python xxx  
  