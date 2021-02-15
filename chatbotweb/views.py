from django.shortcuts import render
from django.http import HttpResponse
from chatbot.chat import ChatBot
import datetime

currentUserId = ChatBot.getUserByFirstName(firstName='Божидар')

def index(request):
    return render(request, 'index.html')

def api_send_chat(request):

    chatbotResponse = ChatBot.Input(sentence=request.POST.get("input", ""), fromUserId=currentUserId);
    return HttpResponse(chatbotResponse)

def api_get_random_question(request):

    chatbotResponse = ChatBot.getRandomQuestion(forUserId=currentUserId);
    return HttpResponse(chatbotResponse)