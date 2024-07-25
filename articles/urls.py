from django.urls import path
from . import views

urlpatterns = [
    path('', views.Article_View.as_view()),
    path('/detail/<int:article_id>', views.Article_Detail_View.as_view())
]
