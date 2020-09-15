from django.contrib import admin
from django.urls import path,include
from . import views
# home k urls m main contact ,about and supponser wala page rkho ga

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('search/',views.search,name='search'),
    path('login', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('signup', views.handleSignup, name='signup')
]
