from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.home, name='home'),
    path('passwords/', views.password_index, name = 'password-index'),
    path('passwords/<int:password_id>/', views.password_detail, name = 'password-detail'), 
]