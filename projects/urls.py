from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('list/', views.ProjectListView.as_view(), name='projects'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('<int:pk>/complete/', views.close_project, name='close_project'),
    path('skills/', views.get_skills, name='get_skills'),
    path('<int:pk>/skills/add/', views.add_skill, name='add_skill'),
    path('<int:pk>/skills/<int:skill_id>/remove/', views.remove_skill, name='remove_skill'),
    path('<int:pk>/toggle-participate/', views.toggle_participation, name='toggle_participation'),
]
