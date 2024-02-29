# Instructions
1. ```git clone git@github.com:mbgoodguy/django_ecom.git```
2. Build the project using Docker Compose: ```sudo docker-compose build```
3. Run the project: ```sudo docker-compose up```
4. Create a superuser using after running the project: ```sudo docker exec -it bigcorp-backend python manage.py createsuperuser```
5. Login as superuser to http://127.0.0.1:8000/admin/ with your credentials and create at least one category for products.
6. Generate fake products: ```sudo docker exec -it bigcorp-backend python manage.py fakerproducts```. You will see 'Products in DB: 20' in console.

## Technologies in project
- Python
- JavaScript
- Ajax
- CSS
- HTML
- Postgres
- Celery
- Redis
- Django
- Django Rest Framework
- Nginx
- Gunicorn
- Swagger and Redoc Docs
- Stripe
- Docker
- Git
