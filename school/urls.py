import school.views as views
from django.urls import path
from school.apps import SchoolConfig
from rest_framework.routers import DefaultRouter
from users.views import PaymentCreateAPIView

# Пространство имен позволяет уникально идентифицировать URL конкретного приложения,
# даже если в проекте есть другие приложения с одинаковыми именами URL-путей
app_name = SchoolConfig.name

router = DefaultRouter()

router.register("courses", views.CourseViewSet, basename="courses")

urlpatterns = [
    path(
        "course/<int:course_id>/payment/",
        PaymentCreateAPIView.as_view(),
        name="create-payment",
    ),
    path("lessons/", views.LessonListAPIView.as_view(), name="lessons"),
    path("lessons/create/", views.LessonCreateAPIView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/", views.LessonDetailAPIView.as_view(), name="lessons_detail"
    ),
    path(
        "lessons/update/<int:pk>/",
        views.LessonUpdateAPIView.as_view(),
        name="lessons_update",
    ),
    path(
        "lessons/delete/<int:pk>/",
        views.LessonDeleteAPIView.as_view(),
        name="lessons_delete",
    ),
    path("subscription/", views.SubscriptionAPIView.as_view(), name="subscription"),
] + router.urls
