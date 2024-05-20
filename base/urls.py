from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('get_query/',  views.search, name='search'), # ye main.html api call krny k liye add kiya 
    # path('register', views.registerPage, name="register"),
    path('lecture/', views.topic, name='lecture'),
    path('search/', views.search, name='search'),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
     path('update-user/', views.updateUser, name="update-user"),

   
]


