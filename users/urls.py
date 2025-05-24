import users.views as views
from django.urls import path
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('users/<str:email>/', views.CustomUserDetailAPIView.as_view(), name="users_detail"),
    path("users/", views.CustomUserListAPIView.as_view(), name="users"),
    path("users/create/", views.CustomUserCreateAPIView.as_view(), name="users_create"),
    path("users/update/<str:email>/", views.CustomUserUpdateAPIView.as_view(), name="users_update"),
    path("users/delete/<str:email>/", views.CustomUserDeleteAPIView.as_view(), name="users_delete"),
]
