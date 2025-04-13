import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .chatbot import *

# Create your views here.


def index(request):
    return render(request, "webapp/index.html")


@csrf_exempt
def chat(request):
    if request.method == "POST":
        message = json.loads(request.body).get("message")
        # scrape_internshala()
        response = chat_bot(message)

        return JsonResponse({"response": response})
    return JsonResponse({"message": "Only Post request"})
