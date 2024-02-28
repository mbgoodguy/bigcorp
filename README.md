1. ```git clone git@github.com:mbgoodguy/django_ecom.git```
2. Build the project using Docker Compose: ```sudo docker-compose build```
3. Run the project: ```sudo docker-compose up```

Ceate a superuser using after running the project: ```sudo docker exec -it bigcorp-backend python manage.py createsuperuser```
Login as superuser to http://127.0.0.1:8000/admin/
Generate fake products using the following command: ```sudo docker exec -it bigcorp-backend python manage.py fakerproducts```
