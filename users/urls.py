import users.views as views
from django.urls import path
from users.apps import UsersConfig
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView. as_view(), name='token_refresh'),

    path('users/<str:email>/', views.CustomUserDetailAPIView.as_view(), name="users_detail"),
    path("users/", views.CustomUserListAPIView.as_view(), name="users"),
    path("register/", views.CustomUserCreateAPIView.as_view(), name="users_create"),
    path("users/update/<str:email>/", views.CustomUserUpdateAPIView.as_view(), name="users_update"),
    path("users/delete/<str:email>/", views.CustomUserDeleteAPIView.as_view(), name="users_delete"),

    path("payment/", views.PaymentListAPIView.as_view(), name="payment"),
    path("payment/create/", views.PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/<int:pk>/", views.PaymentDetailAPIView.as_view(), name="payment_detail"),
    path("payment/update/<int:pk>/", views.PaymentUpdateAPIView.as_view(), name="payment_update"),
    path("payment/delete/<int:pk>/", views.PaymentDeleteAPIView.as_view(), name="payment_delete"),
]
