from django.urls import path
from .views import *

urlpatterns=[
    path('',home,name='home'),
    path('user_home/',user_home,name='user_home'),
    path('admin_home/',admin_home,name='admin_home'),
    path('reservation/',reservation,name='reservation'),
    path('reserved/',reserved,name='reserved'),
    path('cancle/<int:pk>',cancle,name='cancle'),
    path('view_reservations/',view_reservations,name='view_reservations'),
    path('date_reservation/',date_reservation,name='date_reservation'),
    path('admin_cancle/<int:pk>',admin_cancle,name='admin_cancle'),
    path('admin_modify/<int:pk>',admin_modify,name='admin_modify')
]