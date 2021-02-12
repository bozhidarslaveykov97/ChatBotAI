from django.shortcuts import render
from django.http import HttpResponse
from chatbot.chat import ChatBot

# from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

#
# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, "db.html", {"greetings": greetings})

def api_send_chat(request):

    chatbotResponse = ChatBot.Input(request.POST.get("input", ""));

    return HttpResponse(chatbotResponse)