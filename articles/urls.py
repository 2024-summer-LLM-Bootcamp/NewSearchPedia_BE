from django.urls import path
from . import views

urlpatterns = [
    path('', views.Article_View.as_view())
]
