import random
import json
import torch
import datetime

from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words, tokenize
from chatbotweb.models import User,UserPersonality,ChatbotQuestionSession

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('./chatbot/intents.json', 'r', encoding="utf8") as json_data:
    intents = json.load(json_data)

with open('./chatbot/questions.json', 'r', encoding="utf8") as json_data:
    questions = json.load(json_data)

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

def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
    leadingText = originalText.split(delimeterA)[0]
    trailingText = originalText.split(delimterB)[1]

    return leadingText + replacementText + trailingText

class ChatBot():

    def saveTheAnswerFromQuestion(answer, fromUser):

        return 'Добре! :)'


    def getRandomQuestion(forUser):

        for question in questions['questions']:

            randomQuestion = random.choice(question['patterns'])
            randomQuestion = replaceTextBetween(randomQuestion, '{','}', '')

            try:
                currentUser = User.objects.get(id=1)
            except User.DoesNotExist:
                currentUser = False
            if (currentUser == False):
                currentUser = User.objects.create(first_name=forUser, registration_date=datetime.datetime.now())

            ChatbotQuestionSession.objects.create(user=currentUser, question=randomQuestion, asked_question_date=datetime.datetime.now())

            return bot_name + ": <br />" + randomQuestion

    def Input(sentence, fromUser):

        userId = 1
        # currentUser = User.objects.filter(id=1)
        try:
            currentUserSession = ChatbotQuestionSession.objects.filter(user=userId)
            hasChatbotQuestionSession = 1
        except ChatbotQuestionSession.DoesNotExist:
            hasChatbotQuestionSession = 0
        if (hasChatbotQuestionSession > 0):
            # Save the answer
            ChatbotQuestionSession.objects.filter(user=userId).delete()
            return ChatBot.saveTheAnswerFromQuestion(sentence, fromUser)

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