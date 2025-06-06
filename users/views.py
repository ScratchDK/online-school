from rest_framework import generics
from users.models import CustomUser, Payment
from school.models import Course
from users.permissions import IsOwnerOrAdmin, IsProfileOwner
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from users.serializers import CustomUserSerializer, PaymentSerializer, PublicUserSerializer, PrivateUserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from school.paginators import MyPagination
from django.shortcuts import get_object_or_404
from users.services import create_stripe_product, create_stripe_price, create_checkout_session
from rest_framework.response import Response


# class CustomUserViewSet(viewsets.ModelViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
#     lookup_field = 'email'


# POST
class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        user = serializer.save(is_active=True)
        user.set_password(password)
        user.save()


# PATCH
class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'email'
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


# DELETE
class CustomUserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'email'
    permission_classes = [IsAuthenticated, IsAdminUser]


# GET
class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    pagination_class = MyPagination
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]


# GET
class CustomUserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'email'
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return PrivateUserSerializer
        return PublicUserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsProfileOwner()]


# Payment
class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Создаем продукт в Stripe если его нет
        if not course.stripe_product_id:
            course.stripe_product_id = create_stripe_product(course)
            course.save()

        # Создаем цену если ее нет или изменилась цена
        if not course.stripe_price_id:
            course.stripe_price_id = create_stripe_price(course)
            course.save()

        # Получаем ссылку на оплату
        checkout_url = create_checkout_session(course, user)

        return Response({'url': checkout_url})


# PATCH
class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


# DELETE
class PaymentDeleteAPIView(generics.DestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    pagination_class = MyPagination
    queryset = Payment.objects.all()

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['payment_date']
    search_fields = ['paid_course', 'paid_lesson', 'payment_method']


class PaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
