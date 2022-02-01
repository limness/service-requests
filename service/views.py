
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from .models import User, DiagnosticRequest
from .serializers import RegistrationSerializer
#

def index(req):
    return render(req, 'index.html')


# class AuthUserView(CreateAPIView):
#
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer

class RegisterUserView(CreateAPIView):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

class RegisterCar(CreateAPIView):

    queryset = DiagnosticRequest.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RegistrationSerializer
