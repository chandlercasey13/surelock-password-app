from django.urls import path
from . import views  # Import views to connect routes to view functions
from .views import CrudView, simple_password_create, signup, ajax_login_view, bulk_delete_view

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path('passwords/', views.CrudView.as_view(), name='password-list'),  # List, create, update, delete
    path('passwords/<int:id>/', views.CrudView.as_view(), name='password-detail'),  # Update and delete specific password

    path('signup/', views.signup, name='signup'),  # User signup
    path("accounts/signup/", views.signup, name="signup"),
    
    path('passwords/create/', views.simple_password_create, name='simple-password-create'),  # Separate create view if needed
    path('ajax-login/', views.ajax_login_view, name='ajax_login'),  # AJAX login endpoint
    path('bulk-delete/', bulk_delete_view, name='bulk-delete'),
    path('reveal-password/', views.reveal_password_api, name='reveal_password_api'),
]



 
# from django.urls import path
# from . import views  # Import views to connect routes to view functions
# from .views import check_authentication_status
# from .views import ajax_login_view
# urlpatterns = [
#     path("", views.Home.as_view(), name="home"),
#     path("passwords/", views.CrudView.as_view(), name="password-list"),
#     path("passwords/<int:pk>/", views.PassUpdate.as_view(), name="password-detail"),  # Keep this if you prefer class-based view
#     path("passwords/<int:id>/delete/", views.CrudView.as_view(), name="password-delete"),
#     path("accounts/signup/", views.signup, name="signup"),
#     path("passwords/create/", views.simple_password_create, name="simple_password_create"),
#     path('check-auth-status/', check_authentication_status, name='check_auth_status'),
#     path('ajax-login/', ajax_login_view, name='ajax_login'),
# ]