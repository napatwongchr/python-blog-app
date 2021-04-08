from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db import connections, DataError

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CommentSerializer, PostSerializer
from .models import Post, Comment

import json

@api_view(['GET'])
def comment_list(request, post_id): 
  if request.method == "GET":
    comments = Comment.objects.filter(post_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({ "data": serializer.data })

@api_view(['GET', 'POST'])
@csrf_exempt
def post_list(request):
  if (request.method == "GET"):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({ "data": serializer.data })

  if (request.method == "POST"):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({ "message": "created post successfully." }, status=status.HTTP_201_CREATED)

    return Response({ "message": "created post failed", "errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def single_post_detail(request, post_id):
  if request.method == "GET":
    try:
      post = Post.objects.filter(id=post_id)
      serializer = PostSerializer(post[0])
      return Response({ "data": serializer.data })
    except IndexError:
      return Response({ "message": "post not found" }, status=status.HTTP_404_NOT_FOUND)
  
  if request.method == "PUT":
    try:
      post = Post.objects.filter(id=post_id)[0]
      serializer = PostSerializer(post, data=request.data)

      if serializer.is_valid():
        serializer.save()
        return Response({ "message": "updated post successfully." })
      return Response({ "message": "updated post failed", "errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

    except IndexError:
      return Response({ "message": "post not found" }, status=status.HTTP_404_NOT_FOUND)
  
  if request.method == "DELETE":
    try:
      post = Post.objects.filter(id=post_id)[0]
      post.delete()
      return Response({ "message": "deleted post successfully." })
    except IndexError:
      return Response({ "message": "post not found" }, status=status.HTTP_404_NOT_FOUND)

