from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response({ "message": "register successfully" }, status=status.HTTP_201_CREATED)
  return Response({ "message": "register failed", "errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)