from django.urls import path
from . import views  # Import views to connect routes to view functions


urlpatterns = [


    path('', views.Home.as_view(), name='home'),
    path('passwords/', views.CrudView.as_view(), name = 'password-index'),
    path('passwords/<int:pk>/', views.PasswordUpdate.as_view(), name='password-detail'),

    path("passwords/<int:password_id>/", views.password_detail, name="password-detail"),
    path('passwords/<int:id>/delete/', views.CrudView.as_view(), name='password-delete'),

    




    path(
        "password/<int:pk>/update/",
        views.PasswordUpdate.as_view(),
        name="password-update",
    ),
    # path(
    #     "passwords/<int:pk>/",
    #     views.PasswordDelete.as_view(),
    #     name="password-delete",
    # ),
    path("accounts/signup/", views.signup, name="signup"),
    path('passwords/create/', views.simple_password_create, name='simple_password_create'),
]
