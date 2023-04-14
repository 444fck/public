from django.urls import path
from . import views

app_name = "function"
urlpatterns = [
    path('search/', views.feed_search, name='search'),
    path('list/', views.list, name='list'),
    path('config/',views.config, name='config'),
    path('pause_job/', views.pause_job, name='pause_job'),
    path('resume_job/', views.remuse_job, name='remuse_job'),
    path('stop/', views.stop_all_job, name='stop_job'),
    path('feedback/', views.feedback, name='feedback'),

]
