from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.exceptions import *
from django.db import connections, DataError

from .models import Post

import json


posts = {
    "data": [
        {
            "id": "1",
            "title": "Post #1",
            "content": "This is post #1 content"
        }
    ]
}

@csrf_exempt
def post_list(request):

  if (request.method == "GET"):
    queried_posts = Post.objects.raw('SELECT * FROM posts_post')
    data = [model_to_dict(instance) for instance in queried_posts]

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
    with connections['default'].cursor() as cursor:
      cursor.execute('INSERT INTO posts_post (title, content) VALUES (%s, %s)', [data["title"], data["content"]])
    response = JsonResponse(data={ "message": "created post successfully." })
    response.status_code = 201
    return response

@csrf_exempt
def single_post_detail(request, post_id):
  if request.method == "GET":
    try:
      with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM posts_post WHERE id = %s", [post_id])

        columns = [col[0] for col in cursor.description]
        
        data = [
          dict(zip(columns, row))
          for row in cursor.fetchall()
        ]

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
    post = {}

    for post_item in posts["data"]:
      if post_item["id"] == post_id:
        post = post_item
        break
    
    post["title"] = request_data["title"]
    post["content"] = request_data["content"]
    
    response = JsonResponse(data={ "message": "updated post successfully." })
    response.status_code = 200
    return response
  
  if request.method == "DELETE":
    new_posts = []
    
    for post_item in posts["data"]:
      if post_item["id"] != post_id:
        new_posts.append(post_item)
    
    posts["data"] = new_posts
    response = JsonResponse(data={ "message": "deleted post successfully."})
    response.status = 200
    return response

