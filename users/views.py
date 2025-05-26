from rest_framework import generics
from users.models import CustomUser, Payment
from users.serializers import CustomUserSerializer, PaymentSerializer
from rest_framework.filters import SearchFilter, OrderingFilter


# class CustomUserViewSet(viewsets.ModelViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
#     lookup_field = 'email'


# POST
class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


# PATCH
class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'email'


# DELETE
class CustomUserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'email'


# GET
class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


# GET
class CustomUserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'email'


# Payment
class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


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
    queryset = Payment.objects.all()

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['payment_date']
    search_fields = ['paid_course', 'paid_lesson', 'payment_method']


class PaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
