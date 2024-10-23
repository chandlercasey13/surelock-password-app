from django.urls import path
from . import views  # Import views to connect routes to view functions
from .views import check_authentication_status
from .views import ajax_login_view
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("passwords/", views.CrudView.as_view(), name="password-index"),
    path("passwords/<int:pk>/", views.PassUpdate.as_view(), name="password-detail"),  # Keep this if you prefer class-based view
    path("passwords/<int:id>/delete/", views.CrudView.as_view(), name="password-delete"),
    path("accounts/signup/", views.signup, name="signup"),
    path("passwords/create/", views.simple_password_create, name="simple_password_create"),
    path('check-auth-status/', check_authentication_status, name='check_auth_status'),
    path('ajax-login/', ajax_login_view, name='ajax_login'),
]