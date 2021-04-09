from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer

@api_view(['POST'])
def signup(request):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response({ "message": "register successfully" }, status=status.HTTP_201_CREATED)
  return Response({ "message": "register failed", "errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
  serializer = UserLoginSerializer(data=request.data)
  if serializer.is_valid():
    return Response({ "message": "login successfully", "data": serializer.data }, status=status.HTTP_200_OK)
  return Response({ "message": "login failed", "errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)