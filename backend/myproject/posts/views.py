from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    response = JsonResponse(data=posts)
    response.status_code = 200
    return response

  if (request.method == "POST"):
    data = json.loads(request.body)
    posts["data"].append({ "id": "2", "title": data["title"], "content": data["content"] })
    response = JsonResponse(data={ "message": "created post successfully." })
    response.status_code = 201
    return response

def single_post_detail(request, post_id):
  response = JsonResponse({ "data": {} })

  for post in posts["data"]:
    if post["id"] == post_id:
      response = JsonResponse({ "data": post })
      return response
  
  response.status_code = 404
  return response
