from django.urls import path
from api import views

urlpatterns=[
    path('setState/<int:state>', views.sendCommand)
]