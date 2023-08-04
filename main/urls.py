from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('get-filtered-districts/<int:region_id>/', views.get_filtered_districts, name='get_filtered_districts'),
    path('get-filtered-sectors/<int:district_id>/', views.get_filtered_sectors, name='get_filtered_sectors'),
    path('get-filtered-municipalities/<int:state_id>/', views.get_filtered_municipalities, name='get_filtered_municipalities'),
]