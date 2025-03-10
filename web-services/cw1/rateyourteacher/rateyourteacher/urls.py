"""
URL configuration for rateyourteacher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app import views

urlpatterns = [
    #path("", views.index),  # Redirect to app's urls
    # path("app/", include("app.urls")),
    path("admin/", admin.site.urls),
    path("register/", views.register, name="register"),
    path("login_user/", views.login_user, name="login"),
    path("logout_user/", views.logout_user, name="logout"),
    path("list/", views.list, name="list"),
    path("view/", views.view, name="view"),
    path("average/", views.average, name="average"),
    path("rate/", views.rate, name="rate"),
    path("test/", views.test, name="test"),
    path("get_username/", views.get_username, name="get_username"),

]
