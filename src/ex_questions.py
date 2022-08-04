import googletrans
from googletrans import Translator

class Question: 
    question = None
    answers = None
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers

    def print(self):
        print('Question: ' + self.question)
        print('Answers:')
        for answer in self.answers:
            print(answer[0] + ' ' + str(answer[1]))
   


quests = [
    Question("Question 1", [("Fish", True), ("Turtle", True), ("Frog", False)]),
    Question("Question 2", [("Dog", False), ("Cat", True), ("Cheetah", False)]),
    Question("Question 3", [("Soup", True), ("Cake", True)]),
    Question("Question 4", [("Car", False), ("Plane", True), ("Train", False)])
]

def trans_questions(questions):
    translator = Translator()

    to_trans = []
    for question in questions:
        to_trans.append(question.question)
        for answer in question.answers:
            to_trans.append(answer[0])

    translated = translator.translate(to_trans, dest='de')

    translated_questions = [] 
    for question in questions:
        qtext_ger = next(filter(lambda tr: tr.origin == question.question, translated)).text.replace(')', '')
        answers = []
        for answer in question.answers:
            atex_ger = next(filter(lambda tr: tr.origin == answer[0], translated)).text
            answers.append((atex_ger, answer[1]))
        translated_questions.append(Question(qtext_ger, answers))   

    return translated_questions    



def check_for_mulAns(questions):
    mulAns_count = 0
    for question in questions:
        true_answ = filter(lambda answer: answer[1] == True, question.answers)
        if len(list(true_answ)) > 1:
            print('Question: '+question.question+ ' has more then 1 right answer')
            mulAns_count += 1
    print('Total number of question with mul. right answers: ',mulAns_count)

def count_right_answers(question):
    return len(list(filter(lambda answer: answer[1] == True, question.answers)))



def to_Gift(questions, path_to_file):
    with open(path_to_file, 'w') as f:
        count = 1
        for question in questions:
            f.write('::Question ')
            f.write(str(count))
            f.write(':: ')
            f.write(question.question.replace('\n\n', '\n'))
            f.write('{')
            right_answer_val = round(100/count_right_answers(question),5)
            for answer in question.answers:
                if answer[1] == True:
                   f.write('~%'+str(right_answer_val)+'%')                 
                else:
                   f.write('~%-'+str(right_answer_val)+'%')
                f.write(answer[0])
                f.write(' ')
            f.write('}')
            f.write('\n')
            f.write('\n')
            count += 1

#res = trans_questions(quests)
#for q in res:
#    q.print()
#check_for_mulAns(quests)                  
#to_Gift(quests)
