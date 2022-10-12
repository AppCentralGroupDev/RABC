from django.urls import path
from . import views

urlpatterns = [
	path("register/", views.register, name="register"),
	path("login/", views.login_view, name="login"),
	path("adminregister/", views.adminregister, name="adminregister"),
	path("adminlogin/", views.adminlogin, name="adminlogin"),
	path("dashboard/", views.dashboard, name="dashboard"),
	path("logout/", views.logout_view, name="logout"),
]