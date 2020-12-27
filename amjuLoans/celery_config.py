from django.conf.global_settings import TIME_ZONE

# Celery Settings
CELERY_BROKER_URL = 'redis://:pf97a1c6ee3d7d07775f1247c55defaac265c00705b1d698b33e1a6915f1cda4c@ec2-35-171-105-153.compute-1.amazonaws.com:10879'
CELERY_RESULT_BACKEND = 'redis://:pf97a1c6ee3d7d07775f1247c55defaac265c00705b1d698b33e1a6915f1cda4c@ec2-35-171-105-153.compute-1.amazonaws.com:10879'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
