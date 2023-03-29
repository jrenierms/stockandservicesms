from django.urls import path
from apps.home.views import *

urlpatterns = [
    path('', Home.as_view(), name='index'),
]
