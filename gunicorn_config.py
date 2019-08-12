# encoding: utf-8
import multiprocessing

preload_app = True
chdir = '/var/www/html/ace_office'
bind = "127.0.0.1:9002"
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 5000
user = 'root'
group = 'root'
accesslog = '/var/log/gunicorn/xuetangx_video_log_access.log'
errorlog = '/var/log/gunicorn/xuetangx_video_log_error.log'
