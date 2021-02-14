import random
import json
import torch
import datetime

from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words, tokenize
from chatbotweb.models import User, UserPersonality, ChatbotQuestionSession
from django.template.loader import render_to_string

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('./chatbot/intents.json', 'r', encoding="utf8") as json_data:
    intents = json.load(json_data)

with open('./chatbot/questions.json', 'r', encoding="utf8") as json_data:
    allQuestions = json.load(json_data)

FILE = "./chatbot/data.pth"
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
userId = 1

class ChatBot():

    def saveTheAnswerFromQuestion(answer, fromUserId):

        try:
            currentUserSession = ChatbotQuestionSession.objects.get(user=fromUserId)
            hasChatbotQuestionSession = 1
        except ChatbotQuestionSession.DoesNotExist:
            hasChatbotQuestionSession = 0
        if (hasChatbotQuestionSession > 0):
            UserPersonality.objects.create(user_id=fromUserId, personality_key=currentUserSession.question_key, personality_value=answer)

        ChatbotQuestionSession.objects.filter(user=userId).delete()

        # Whats next?
        getAnsweredQuestion = ChatBot.getQuestionByKey(currentUserSession.question_key)
        try:
            if (getAnsweredQuestion['view_response_after_question']):
                responseAfterQuestion = render_to_string('chatbot_response_views/' + getAnsweredQuestion['view_response_after_question'], {currentUserSession.question_key:answer, 'bot_name':bot_name})
                return responseAfterQuestion
        except:
            return 'Еми.. окей.'
        else:
            return 'Добре! :)'

    def getQuestionByKey(questionKey):
        for questions in allQuestions['questions']:
            return random.choice(questions['patterns'][questionKey])

    def startQuestionSession(selectedQuestion,selectedQuestionKey,forUser):
        try:
            currentUser = User.objects.get(id=1)
        except User.DoesNotExist:
            currentUser = False
        if (currentUser == False):
            currentUser = User.objects.create(first_name=forUser, registration_date=datetime.datetime.now())

        ChatbotQuestionSession.objects.create(user=currentUser, question=selectedQuestion['question'],
                                              question_key=selectedQuestionKey,
                                              asked_question_date=datetime.datetime.now())

        return bot_name + ": <br />" + selectedQuestion['question']

    def getRandomQuestion(forUser):

        selectedQuestion = False
        for questions in allQuestions['questions']:
            patternKeys = []
            for pattern in questions['patterns']:
                patternKeys.append(pattern)
            selectedQuestionKey = random.choice(patternKeys)
            selectedQuestion = random.choice(questions['patterns'][selectedQuestionKey])

        if (selectedQuestion):
            return ChatBot.startQuestionSession(selectedQuestion, selectedQuestionKey, forUser)

    def Input(sentence, fromUser):

        # currentUser = User.objects.filter(id=1)
        try:
            currentUserSession = ChatbotQuestionSession.objects.get(user=userId)
            hasChatbotQuestionSession = 1
        except :
            ChatbotQuestionSession.objects.filter(user=userId).delete()
            hasChatbotQuestionSession = 0

        if (hasChatbotQuestionSession > 0):
            # Save the answer
            return ChatBot.saveTheAnswerFromQuestion(sentence, fromUserId=userId)

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
                    return bot_name + ": <br />" + random.choice(intent['responses'])
        else:
            return ""
