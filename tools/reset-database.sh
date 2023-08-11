find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -path "*/db.sqlite3" -delete
pip uninstall django -y
pip install django
python manage.py makemigrations
python manage.py migrate
sqlite3 "db.sqlite3" ".param set :id %1" ".read tools/create-database-mock.sql"
