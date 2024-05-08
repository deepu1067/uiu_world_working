from django.apps import AppConfig
from threading import Thread
from .helpers import *
import sys
has_been_run = False

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        global has_been_run
        if 'runserver' in sys.argv and not has_been_run:
            has_been_run = True
            if not os.path.exists("api/static/journal.pkl"):
                thread = Thread(target=scrape_paper("https://www.uiu.ac.bd/research/journal-paper/", "journal"))
                thread.start()
            
            get_jobs()
            get_notice()