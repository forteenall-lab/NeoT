python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
echo from django.contrib.auth.models import User; User.objects.create_superuser('admin', None, 'admin') | python3 manage.py shell
set /P tmp=insert inter key for exit ...