from django.urls import path
from .views import get_user, create_user, get_all_machine_status
from .views import get_l2_machine_status,create_CNCMachine,get_all_CNCMachine,get_CNCMachine,create_CNCMachine_batch
from .views import get_MachineRealtimeStatus,get_l1_machine_status

urlpatterns = [
    path('users/<int:pk>', get_user, name='get_user'),
    path('users/create/', create_user, name='create_user'),
    path('machine-status/', get_all_machine_status, name='get_all_machine_status'),
    path('l2-machine-status/', get_l2_machine_status, name='get_l2_machine_status'),
    path('l1-machine-status/', get_l1_machine_status, name='get_l1_machine_status'),
    path('CNCMachine/create/', create_CNCMachine, name='create_CNCMachine'),
    path('CNCMachine/create-batch/', create_CNCMachine_batch, name='create_CNCMachine_batch'),
    path('CNCMachine/list/', get_all_CNCMachine, name='get_all_CNCMachine'),
    path('CNCMachine/get/<int:machine_id>', get_CNCMachine, name='get_CNCMachine'),
    path('MachineRealtimeStatus',get_MachineRealtimeStatus,name='get_MachineRealtimeStatus')
]
