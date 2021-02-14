import json
import random

with open('./chatbot/questions.json', 'r', encoding="utf8") as json_data:
    allQuestions = json.load(json_data)

randomQuestion = False

for questions in allQuestions['questions']:

    patternKeys = []
    for pattern in questions['patterns']:
        patternKeys.append(pattern)

    selectedQuestion = questions['patterns'][random.choice(patternKeys)]

    print(selectedQuestion)


