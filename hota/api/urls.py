from django.urls import path
from .views import get_user , create_user ,get_all_machine_status

urlpatterns= [
    path('users/<int:pk>', get_user, name='get_user'),
    path('users/create/', create_user, name='create_user'),
    path('machine-status/', get_all_machine_status, name='get_all_machine_status'),
]