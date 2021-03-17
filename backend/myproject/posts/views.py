from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from django.core import serializers
from django.db import connections

from .models import Post

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
    with connections['default'].cursor() as cursor:
      cursor.execute("SELECT * FROM posts_post")

      columns = [col[0] for col in cursor.description]

      data = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
      ]
   

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
    posts["data"].append({ "id": "2", "title": data["title"], "content": data["content"] })
    response = JsonResponse(data={ "message": "created post successfully." })
    response.status_code = 201
    return response

@csrf_exempt
def single_post_detail(request, post_id):
  if request.method == "GET":
    response = JsonResponse({ "data": {} })

    for post in posts["data"]:
      if post["id"] == post_id:
        response = JsonResponse({ "data": post })
        return response
    
    response.status_code = 404
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

