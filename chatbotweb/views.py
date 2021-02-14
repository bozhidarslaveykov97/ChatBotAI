from django.shortcuts import render
from django.http import HttpResponse
from chatbot.chat import ChatBot

def index(request):
    return render(request, 'index.html')

def api_send_chat(request):
    chatbotResponse = ChatBot.Input(request.POST.get("input", ""));
    return HttpResponse(chatbotResponse)

def api_get_random_question(request):

    questionFor = 'Божидар';

    chatbotResponse = ChatBot.getRandomQuestion(forUser=questionFor);
    return HttpResponse(chatbotResponse)