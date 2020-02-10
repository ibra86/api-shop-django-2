git init
git ls-files
docker exec -it <cont_id> bash


virtualenv -p python3 venv
pip install -r requirements.txt

django-admin startproject config .
python manage.py startapp app
python manage.py runserver 0:8000

update INSTALLED_APPS with module containing models

#quick check status of the resource
curl -s -o /dev/null -w "%{http_code}\n" localhost:8000


