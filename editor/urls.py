from editor.views import random_entry
from os import name
import random
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entry/<str:entry>', views.show_entry, name='entry'),
    path('newEntry/', views.newEntry, name='newEntry'),
    path('random',views.random_entry, name='random'),
    path('search', views.search, name='search'),
    path('delete/<str:entry>', views.delete, name='delete'),
    path('entry/<str:entry>/edit', views.edit, name='editEntry')
]