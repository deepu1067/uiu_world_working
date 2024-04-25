from django.urls import path
from . import views

urlpatterns = [
    path('notice/', views.notice, name='notie-api'),
]