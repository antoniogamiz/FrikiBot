#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

#Aux function
def readJSON(filepath):
    try:
        with open(filepath, 'r') as file:
            items_read = json.load(file)
        return items_read
    except:
        return []

def isRepeated(data, o):
    index=0
    for d in data:
        if d[0] == o:
            return index
        else:
            index+=1
    else:
        return -1

class QuestionsManagement:
    def __init__(self):
        #Read questions stored previously
        self.questions_answered = readJSON("/home/antonio/bot/FrikiBot/JSON/questions_answered.json")
        self.questions_unanswered = readJSON("/home/antonio/bot/FrikiBot/JSON/questions_unanswered.json")
        self.x=0

    #Returns the position of the answer in the page, if the answer doesnt exist, returns -1.
    def getAnswer(self, question, first_answer, second_answer, third_answer, forth_answer):
        #Current question on bot-spider.
        self.current_question = [question, first_answer, second_answer, third_answer, forth_answer]
        for q in self.questions_answered:
            if question == q[0]:
                if q[1] == self.current_question[1]:
                    return [1, 1]
                elif q[1] == self.current_question[2]:
                    return [1, 2]
                elif q[1] == self.current_question[3]:
                    return [1, 3]
                else:
                    return [1, 4]
        else:
            for uq in self.questions_unanswered:
                if question == uq[0]:
                    for x in range(1, 5):
                        if not uq[x][1]:
                            available_answer=uq[x][0]
                            return [0, x]
            else:
                return [0, -1]
        self.backup()
    def getPos(self, data, question):
        i=0
        for q in data:
            if q[0] == question:
                break
            else:
                i+=1
        return i

    def processQuestion(self, index, available, correct):
        if not available:
            if index == -1 and correct:
                self.questions_answered.append([self.current_question[0], self.current_question[index]])
            elif index == -1 and not correct:
                new_question = [self.current_question[0], [self.current_question[1], 0], [self.current_question[2], 0], [self.current_question[3], 0], [self.current_question[4], 0]]
                new_question[index][1]=1
                self.questions_unanswered.append(new_question)
            elif index != -1 and not correct:
                self.questions_unanswered[self.getPos(self.questions_unanswered, self.current_question[0])][index][1]=1
            else:
                self.questions_unanswered.pop(self.getPos(self.questions_unanswered, self.current_question[0]))
                self.questions_answered.append([self.current_question[0], self.current_question[index]])

            self.x+=1
            if self.x < 1000:
                self.backup()

            if self.x == 1000:
                self.x=0
    def backup(self):
        with open("/home/antonio/bot/FrikiBot/JSON/questions_answered.json", 'w') as file:
            json.dump(self.questions_answered, file)
        with open("/home/antonio/bot/FrikiBot//JSON/questions_unanswered.json", 'w') as file:
            json.dump(self.questions_unanswered, file)
