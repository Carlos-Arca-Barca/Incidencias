from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path("calidad/", views.calidad, name="calidad"),
    path("calidad/nuevo/", views.calidad_nuevo, name="calidad_nuevo"),
    path("calidad/<int:id>/", views.calidad_ver, name="calidad_ver"),
    path("calidad/<int:id>/editar/", views.calidad_editar, name="calidad_editar"),
    path("calidad/<int:id>/eliminar/", views.calidad_eliminar, name="calidad_eliminar"),

    # 🔐 AUTH (AÑADIR ESTO)
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]