from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update', views.update, name='update'),
    path('getatt', views.getAtt, name='getatt'),

]
