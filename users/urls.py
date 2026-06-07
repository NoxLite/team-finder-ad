from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('list/', views.UserListView.as_view(), name='participants'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='participant_detail'),
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.profile_change_view, name='edit_profile'),
    path('change-password/', views.password_change_view, name='change_password'),
]
