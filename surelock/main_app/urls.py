from django.urls import path
from . import views  # Import views to connect routes to view functions

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('passwords/', views.password_index, name = 'password-index'),
    path('passwords/<int:password_id>/', views.password_detail, name = 'password-detail'), 
    path(
        "password/<int:pk>/update/",
        views.PasswordUpdate.as_view(),
        name="password-update",
    ),
    path(
        "passwords/<int:pk>/delete/",
        views.PasswordDelete.as_view(),
        name="password-delete",
    ),
    
]
