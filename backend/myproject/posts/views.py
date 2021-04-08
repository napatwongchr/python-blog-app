from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db import connections, DataError

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CommentSerializer
from .models import Post, Comment

import json

@api_view(['GET'])
def comment_list(request, post_id): 
  if request.method == "GET":
    comments = Comment.objects.filter(post_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({ "data": serializer.data })

@csrf_exempt
def post_list(request):

  if (request.method == "GET"):
    queried_posts = Post.objects.all()

    data = list(queried_posts.values())

    response_data = {}
    response_data['data'] = data

    response = HttpResponse(
      json.dumps(response_data),
      content_type='application/json'
    ) 
    
    response.status_code = 200
    return response

  if (request.method == "POST"):
    data = json.loads(request.body)
    
    post = Post(
      title=data["title"],
      content=data["content"]
    )

    post.save()

    response = JsonResponse(data={ "message": "created post successfully." })
    response.status_code = 201
    return response


@csrf_exempt
def single_post_detail(request, post_id):
  if request.method == "GET":
    try:
      queried_post = Post.objects.filter(id=post_id)
      data = queried_post.values()[0]
    except DataError:
      response_data = {}
      response_data['message'] = "Invalid request"
      response_data['data'] = []

      response = HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
      )
      response.status_code = 400
      return response


    response_data = {}
    response_data['data'] = data

    response = HttpResponse(
      json.dumps(response_data),
      content_type='application/json'
    ) 
    
    response.status_code = 200
    
    return response
  
  if request.method == "PUT":
    request_data = json.loads(request.body)
    
    try:
      queried_post = Post.objects.filter(id=post_id)[0]
      queried_post.title = request_data["title"]
      queried_post.content = request_data["content"]
      queried_post.save()

    except DataError:
      response_data = {}
      response_data['message'] = "Invalid request"

      response = HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
      )
      response.status_code = 400
      return response
    
    response = JsonResponse(data={ "message": "updated post successfully." })
    response.status_code = 200
    return response
  
  if request.method == "DELETE":
    try:
      queried_post = Post.objects.filter(id=post_id)[0]
      queried_post.delete()
    except DataError:
      response_data = {}
      response_data['message'] = "Invalid request"

      response = HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
      )
      response.status_code = 400
      return response

    response = JsonResponse(data={ "message": "deleted post successfully."})
    response.status = 200
    return response

