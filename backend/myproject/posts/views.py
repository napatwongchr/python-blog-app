from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

posts = {
    "data": [
        {
            "id": "1",
            "title": "Post #1",
            "content": "This is post #1 content"
        }
    ]
}

def post_list(request):
  response = JsonResponse(data=posts)
  response.status_code = 200
  return response

def single_post_detail(request, post_id):
  response = JsonResponse({ "data": {} })

  for post in posts["data"]:
    if post["id"] == post_id:
      response = JsonResponse({ "data": post })
      return response
  
  response.status_code = 404
  return response
