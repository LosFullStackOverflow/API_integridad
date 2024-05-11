from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.get_all, name="getAllUsers"),
    path('cliente/<str:email>/', views.get_one, name="getOneUsers"),
    path('cliente/', views.create, name="createUser"),
    path('cliente/update/<str:email>/', views.update, name="updateUser"),
]
