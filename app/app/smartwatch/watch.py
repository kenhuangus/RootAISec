import signal
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.core.management import call_command
import os
from multiprocessing import Process
from . import settings
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

gunicorn_process = None
daphne_process = None

def get_project_name():
    settings_module = os.getenv('DJANGO_SETTINGS_MODULE')
    if settings_module is not None:
        project_name = settings_module.split('.')[0]
        return project_name
    else:
        return None


def start_gunicorn(hostname=None, port=None):
    hostname = hostname or settings.SMARTWATCH_GUNICORN_HOST
    port = port or settings.SMARTWATCH_GUNICORN_PORT
    os.system(f'gunicorn -b {hostname}:{port} {get_project_name()}.wsgi:application')

def start_daphne(hostname=None, port=None):
    hostname = hostname or settings.SMARTWATCH_DAPHNE_HOST
    port = port or settings.SMARTWATCH_DAPHNE_PORT
    os.system(f'daphne -b {hostname} -p {port} {get_project_name()}.asgi:application')

import psutil

def kill_process_and_children(pid):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()

def kill_gunicorn():
    global gunicorn_process
    if gunicorn_process is not None:
        print('killing gunicorn')
        kill_process_and_children(gunicorn_process.pid)
        gunicorn_process = None
        print('killed gunicorn')
    else:
        print('not killing gunicorn')

def kill_daphne():
    global daphne_process
    if daphne_process is not None:
        print('killing daphne')
        kill_process_and_children(daphne_process.pid)
        daphne_process = None
        print('killed daphne')
    else:
        print('not killing daphne')

def start_servers():
    global gunicorn_process
    global daphne_process
    if settings.SMARTWATCH_USE_GUNICORN:
        kill_gunicorn()
        print('starting gunincorn')
        gunicorn_process = Process(target=start_gunicorn)
        gunicorn_process.start()
    if settings.SMARTWATCH_USE_DAPHNE:
        kill_daphne()
        print('starting daphne')
        daphne_process = Process(target=start_daphne)
        daphne_process.start()
    print('started the servers')


class ServerHandler(FileSystemEventHandler):
    DEBOUNCE_SECONDS = 1
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_modified = time.time()

    def on_modified(self, event):
        current_time = time.time()
        if current_time - self.last_modified < self.DEBOUNCE_SECONDS:
            return
        self.last_modified = current_time

        should_restart = event.src_path.endswith('.py')
        if 'requirements.txt' in event.src_path:
            logging.info(f'{event.src_path} has been modified. Installing requirements...')
            should_restart = True
            os.system('pip install -r requirements.txt')
        if 'templates' in event.src_path:
            should_restart = True
        if settings.SMARTWATCH_MIGRATE and 'migrations' in event.src_path:
            should_restart = False
            logging.info(f'{event.src_path} has been modified. Running migrations...')
            call_command('migrate')
        if settings.SMARTWATCH_COLLECT_STATIC and 'static' in event.src_path:
            logging.info(f'{event.src_path} has been modified. Collecting static files...')
            call_command('collectstatic', '--noinput')
        if should_restart:
            logging.info(f'{event.src_path} has been modified. Restarting server...')
            start_servers()


def watch_files():
    server_handler = ServerHandler()
    observer = Observer()
    observer.schedule(server_handler, '.', recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
