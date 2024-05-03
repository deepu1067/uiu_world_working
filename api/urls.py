from django.urls import path
from . import views

urlpatterns = [
    path('notice/', views.notice, name='notie-api'),
    path('journal/', views.journal, name='journal-api'),
    path('jobs/', views.jobs, name='jobs-api')
]