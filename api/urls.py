from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('clientes/', views.get_all, name="getAllUsers"),
    path('cliente/<str:email>/', views.get_one, name="getOneUsers"),
    path('cliente/', views.create, name="createUser"),
    path('cliente/update/<str:email>/', views.update, name="updateUser"),
    path('estado/<str:email>/', views.get_estadoPOST, name="estadoPost"),
    path('estado/<str:email>/get/', views.get_estado, name="estado"),

]
