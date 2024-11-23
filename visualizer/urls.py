from django.urls import path

from visualizer import views

app_name = 'visualizer'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('create/prompt', views.create_prompt, name='create_prompt'),
    path('create/upload', views.create_upload, name='create_upload'),
]
