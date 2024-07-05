from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
    path('containers/', views.ContainerListCreate.as_view(), name='container-list-create'),
    path('containers/<int:pk>/', views.ContainerDetail.as_view(), name='container-detail'),
    path('create_project/', views.ProjectCreateView.as_view(), name='create_project'),
    path('project/<str:id>/start/', views.ProjectStartView.as_view(), name='project-start'),
    path('project/<str:id>/stop/', views.ProjectStopView.as_view(), name='project-stop'),
    path('project/<str:id>/restart/', views.ProjectRestartView.as_view(), name='project-restart'),
    path('project/<str:id>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),

]
