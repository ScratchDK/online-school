import school.views as views
from django.urls import path
from school.apps import SchoolConfig
from rest_framework.routers import DefaultRouter

app_name = SchoolConfig.name

router = DefaultRouter()

router.register("courses", views.CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", views.LessonListAPIView.as_view(), name="lessons"),
    path("lessons/create/", views.LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/", views.LessonDetailAPIView.as_view(), name="lessons_detail"),
    path("lessons/update/<int:pk>/", views.LessonUpdateAPIView.as_view(), name="lessons_update"),
    path("lessons/delete/<int:pk>/", views.LessonDeleteAPIView.as_view(), name="lessons_delete"),
    path("subscription/", views.SubscriptionAPIView.as_view(), name="subscription"),
] + router.urls
