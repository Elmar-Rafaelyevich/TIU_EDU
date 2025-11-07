from django.urls import path
from main import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('group/add/', views.create_group, name='create_group'),
    path('group/<int:pk>/edit/', views.edit_group, name='edit_group'),
    path('group/<int:pk>/delete/', views.delete_group, name='delete_group'),
    path('group/<int:group_pk>/upload/', views.upload_presentations, name='upload_presentations'),
    path('presentation/<int:pk>/delete/', views.delete_presentation, name='delete_presentation'),
]
