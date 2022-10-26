web: gunicorn newapi.wsgi --timeout 500 --keep-alive 5 --log-level debug
python manage.py collectstatic --noinput
manage.py migrate