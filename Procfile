web: python stock_control_lab/manage.py runserver
worker: PYTHONPATH=$PYTHONPATH:./stock_control_lab DJANGO_SETTINGS_MODULE=stock_control_lab.config.settings celery -A stock_control_lab.config worker -l info
beat: PYTHONPATH=$PYTHONPATH:./stock_control_lab DJANGO_SETTINGS_MODULE=stock_control_lab.config.settings celery -A stock_control_lab.config beat -l info
