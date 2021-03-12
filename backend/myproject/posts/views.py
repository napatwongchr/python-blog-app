from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

posts = {
    "data": [
        {
            "id": 1,
            "title": "Post #1",
            "content": "This is post #1 content"
        }
    ]
}

def post_list(request):
    response = JsonResponse(posts)
    response.status_code = 200
    return response