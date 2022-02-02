
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from .models import User, DiagnosticRequest
from .serializers import UserRegistrationSerializer
from .serializers import CarRegistrationSerializer
from .serializers import UpdateFullNameSerializer
from .serializers import UpdateCarSerializer
from .serializers import ExpertListSerializer
#

def index(req):
    return render(req, 'index.html')

#####

class RegisterUserView(CreateAPIView):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

class RegisterCarView(CreateAPIView):

    queryset = DiagnosticRequest.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CarRegistrationSerializer

class ExpertsListView(ListAPIView):

    queryset = User.objects.filter(is_expert=True)
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpertListSerializer

class UpdateNameView(UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UpdateFullNameSerializer
    permission_classes = (IsAuthenticated,)

class UpdateCarView(UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UpdateCarSerializer
    permission_classes = (IsAuthenticated,)
