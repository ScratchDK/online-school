from rest_framework.response import Response
from rest_framework import viewsets, generics
from school.models import Course, Lesson, Subscription
from school.serializers import CourseSerializer, LessonSerializer
from school.permissions import IsAdminOrModerator, IsOwner, IsModerator
from rest_framework.permissions import IsAdminUser
from school.paginators import MyPagination
from school.services import send_mailing

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MyPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAdminUser | IsOwner]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsAdminOrModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        # Получаем курс до обновления
        course = self.get_object()

        # Получаем всех подписанных пользователей
        subscribed_users = course.subscription.all().select_related("user")
        user_emails = [sub.user.email for sub in subscribed_users]

        # Асинхронный вызов
        send_mailing.delay(user_emails, course.title)

        response = super().update(request, *args, **kwargs)

        return response


# Lesson
# POST
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# PATCH
class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminOrModerator | IsOwner]


# DELETE
class LessonDeleteAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner]


# GET
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = MyPagination
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminOrModerator | IsOwner]


# GET
class LessonDetailAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminOrModerator | IsOwner]


class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item, created = Subscription.objects.get_or_create(
            user=user, course=course_item
        )

        if not created:
            subs_item.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка добавлена"

        return Response({"message": message})
