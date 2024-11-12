import string
from django.contrib.auth import authenticate, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DepartmentSerializer, Patient_RecordSerializer, UserSerializer
from .models import Department, Doctor, Patient, Patient_Record, User
from rest_framework import permissions, status, generics
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, IsAuthenticatedOrTokenHasScope
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta, datetime

@api_view(['POST'])
def user_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        if 'password' in request.data:
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
        # token = Token.objects.create(user=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    application = Application.objects.get(name='grey') 

    if user is not None:
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            expires=timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            token=get_random_string(30, string.ascii_lowercase+string.ascii_uppercase+string.digits),
            scope='read write'
        )
        
        rtoken = RefreshToken.objects.create(
            user=user,
            access_token=access_token,
            application=application,
            token=get_random_string(30, string.ascii_lowercase+string.ascii_uppercase+string.digits)
        )
    token = AccessToken.objects.filter(user=user, expires__gt=datetime.now())
    rtoken = RefreshToken.objects.filter(user=user, expires__gt=datetime.now())
    return JsonResponse({
        'access_token': token[0].token,
        'scope': token[0].scope,
        'Refresh Token': rtoken[0].token,
    })

@api_view(['POST'])
def user_logout(request):
    if request.user:
        model = AccessToken.objects.get(user=request.user)
        model.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


class ListDoctors(generics.ListCreateAPIView):
    permission_classes = [TokenHasReadWriteScope]
    queryset = Doctor.doctor.all()
    serializer_class = UserSerializer

class ListPatients(generics.ListCreateAPIView):
    queryset = Patient.patient.all()
    serializer_class = UserSerializer
    permission_classes = [TokenHasReadWriteScope]

class ListDepartments(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [TokenHasReadWriteScope]

@api_view(['GET', 'PUT', 'DELETE'])
def DepartmentDetails(request, pk):
    pass


@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def patient_details(request, pk):
    model = Patient.patient.get(pk=pk)
    serializer = UserSerializer(model, many=True)
    
    if request.method == 'GET':
        return Response(serializer.data)

    elif request.method == 'DELETE':
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = UserSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def doctor_details(request, pk):
    model = Doctor.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserSerializer(model)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListPatientRecords(generics.ListCreateAPIView):
    serializer_class = Patient_RecordSerializer
    queryset = Patient_Record.objects.all()
    permission_classes = [TokenHasReadWriteScope]
