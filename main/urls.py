from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('get_districts/', views.get_filtered_districts, name='get_districts'),
]