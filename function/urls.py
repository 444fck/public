from django.urls import path
from . import views

app_name = "function"
urlpatterns = [
    path('search/', views.feed_search, name='search'),
    path('list/', views.list, name='list'),
    path('config/',views.config, name='config'),
    path('chart/', views.chart, name='chart'),
    path('feedback/', views.feedback, name='feedback')
]
