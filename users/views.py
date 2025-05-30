from rest_framework import generics
from users.models import CustomUser, Payment
from users.permissions import IsOwnerOrAdmin, IsProfileOwner
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from users.serializers import CustomUserSerializer, PaymentSerializer, PublicUserSerializer, PrivateUserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter


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
