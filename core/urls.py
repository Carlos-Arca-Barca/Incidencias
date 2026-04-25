from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("calidad/", views.calidad_list, name="calidad_list"),
    path("calidad/grid/", views.calidad_grid, name="calidad_grid"),
]