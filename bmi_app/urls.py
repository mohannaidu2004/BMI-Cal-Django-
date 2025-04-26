from django.urls import path
from . import views

app_name = 'bmi_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate/', views.calculate_bmi, name='calculate'),
]