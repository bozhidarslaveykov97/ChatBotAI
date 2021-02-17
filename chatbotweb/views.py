from django.shortcuts import render
from django.http import HttpResponse
from chatbot.chat import ChatBot
import datetime

def index(request):
    return render(request, 'index.html')

def api_send_chat(request):

    currentUserId = ChatBot.getUserByFirstName(firstName='Божидар')

    chatbotResponse = ChatBot.Input(sentence=request.POST.get("input", ""), fromUserId=currentUserId);
    return HttpResponse(chatbotResponse)

def api_get_random_question(request):

    currentUserId = ChatBot.getUserByFirstName(firstName='Божидар')

    chatbotResponse = ChatBot.getRandomQuestion(forUserId=currentUserId);
    return HttpResponse(chatbotResponse)