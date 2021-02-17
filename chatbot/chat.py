import random
import json
import torch
import datetime

from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words, tokenize
from chatbotweb.models import User, UserPersonality, ChatbotQuestionSession, ChatbotConversations, ChatbotPersonality
from django.template.loader import render_to_string

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding="utf8") as json_data:
    intents = json.load(json_data)

with open('questions.json', 'r', encoding="utf8") as json_data:
    allQuestions = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Ванеса"


class ChatBot():

    def getUserByFirstName(firstName):
        try:
            currentUser = User.objects.get(id=1)
        except User.DoesNotExist:
            currentUser = False
        if (currentUser == False):
            currentUser = User.objects.create(first_name=firstName, registration_date=datetime.datetime.now())

        return currentUser

    def saveTheAnswerFromQuestion(answer, fromUserId):

        try:
            currentUserSession = ChatbotQuestionSession.objects.get(user=fromUserId)
            hasChatbotQuestionSession = 1
        except ChatbotQuestionSession.DoesNotExist:
            hasChatbotQuestionSession = 0
        if (hasChatbotQuestionSession > 0):
            UserPersonality.objects.create(user=fromUserId, personality_key=currentUserSession.question_key,
                                           personality_value=answer)

        ChatbotQuestionSession.objects.filter(user=fromUserId).delete()

        # Whats next?
        getAnsweredQuestion = ChatBot.getQuestionByKey(currentUserSession.question_key)
        try:
            if (getAnsweredQuestion['view_response_after_question']):
                responseAfterQuestion = render_to_string(
                    'chatbot_response_views/' + getAnsweredQuestion['view_response_after_question'],
                    {currentUserSession.question_key: answer, 'bot_name': bot_name})
                return responseAfterQuestion
        except:
            return 'Еми.. окей.'
        else:
            return 'Добре! :)'

    def getQuestionByKey(questionKey):
        for questions in allQuestions['questions']:
            return random.choice(questions['patterns'][questionKey])

    def startQuestionSession(selectedQuestion, selectedQuestionKey, forUserId):

        ChatbotQuestionSession.objects.create(user=forUserId, question=selectedQuestion['question'],
                                              question_key=selectedQuestionKey,
                                              asked_question_date=datetime.datetime.now())

        return bot_name + ": <br />" + selectedQuestion['question']

    def getRandomQuestion(forUserId):

        getUserPersonalities = UserPersonality.objects.filter(user_id=forUserId)

        selectedQuestion = False
        for questions in allQuestions['questions']:
            patternKeys = []
            for pattern in questions['patterns']:
                addThisPattern = True
                for userPersonality in getUserPersonalities:
                    if (pattern == userPersonality.personality_key):
                        addThisPattern = False
                        break
                if (addThisPattern):
                    patternKeys.append(pattern)
            if (patternKeys):
                selectedQuestionKey = random.choice(patternKeys)
                selectedQuestion = random.choice(questions['patterns'][selectedQuestionKey])
            else:
                return ""

        if (selectedQuestion):
            return ChatBot.startQuestionSession(selectedQuestion, selectedQuestionKey, forUserId)

    def ParseNeuralNetworkResponse(chatbotResponse):

        try:
            chatbotPersonality = {}
            getChatbotPersonality = ChatbotPersonality.objects.all()
            for getChatbotPersonalityItem in getChatbotPersonality:
                chatbotPersonality[
                    getChatbotPersonalityItem.personality_key] = getChatbotPersonalityItem.personality_value
        except:
            # cant get chat bot personality
            chatbotPersonality = {
                'emotional_status': 'neutral'
            }

        if ("{{chatbot_emotional_status_down}}" in chatbotResponse):
            ChatbotPersonality.objects.filter(personality_key='emotional_status').update(personality_value='angry')
            chatbotResponse = 'Ако обичаш не ме псувай защото ще те блокирам..'

        if ("{{chatbot_emotional_status_up}}" in chatbotResponse):
            ChatbotPersonality.objects.filter(personality_key='emotional_status').update(personality_value='beautifully')
            chatbotResponse = 'Благодаря ти за комплимента.. :)'

        if ("{{chatbot_emotional_status}}" in chatbotResponse):
            chatbotResponse = render_to_string('chatbot_response_views/chatbot_emotional_status.html', {'chatbot_personality':chatbotPersonality})

        if ("{{chatbot_emotional_answer}}" in chatbotResponse):
            chatbotResponse = render_to_string('chatbot_response_views/chatbot_emotional_answer.html', {'chatbot_personality':chatbotPersonality})

        if ("{{chatbot_emotional_status_explain}}" in chatbotResponse):
            chatbotResponse = render_to_string('chatbot_response_views/chatbot_emotional_status_explain.html', {'chatbot_personality':chatbotPersonality})

        return chatbotResponse

    def Input(sentence, fromUserId):

        # Start the conversation
        try:
            findConversation = ChatbotConversations.objects.filter(user=fromUserId, starting_date=datetime.date.today())
        except:
            findConversation = ChatbotConversations.objects.create(user=fromUserId, starting_date=datetime.datetime.now())

        # Check for question sessions
        try:
            currentUserSession = ChatbotQuestionSession.objects.get(user=fromUserId)
            hasChatbotQuestionSession = 1
        except:
            ChatbotQuestionSession.objects.filter(user=fromUserId).delete()
            hasChatbotQuestionSession = 0

        if (hasChatbotQuestionSession > 0):
            # Save the answer
            return ChatBot.saveTheAnswerFromQuestion(sentence, fromUserId=fromUserId)

        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    chatbotResponse = random.choice(intent['responses'])
                    return bot_name + ": <br />" + ChatBot.ParseNeuralNetworkResponse(chatbotResponse)
        else:
            return ""
