from django.urls import path
from expenses import views


app_name= 'expenses'

urlpatterns = [
    path('', views.index, name='expenses'),
]