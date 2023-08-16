find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
pip uninstall django -y
pip install django
python manage.py makemigrations
python manage.py migrate --fake
python manage.py migrate
