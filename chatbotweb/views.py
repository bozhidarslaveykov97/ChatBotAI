from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny

from chatbot.chat import ChatBot
from chatbotweb.serializers import UserSerializer, GroupSerializer, RegisterSerializer

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



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer