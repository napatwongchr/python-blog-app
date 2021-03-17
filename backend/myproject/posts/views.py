from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core import serializers
from django.db import connections, DataError

from .models import Post

import json

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
      print(f"quired_post {data}")
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
      with connections['default'].cursor() as cursor:
        cursor.execute(
          "UPDATE posts_post SET title=%s, content=%s WHERE id=%s;",
          [request_data["title"], request_data["content"], post_id]
        )
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
      with connections['default'].cursor() as cursor:
        cursor.execute(
          "DELETE FROM posts_post WHERE id=%s",
          [post_id]
        )
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

