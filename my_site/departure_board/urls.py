from django.urls import include, path
from departure_board import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('boards', views.boards_json),
    path('departure', views.departure),
]