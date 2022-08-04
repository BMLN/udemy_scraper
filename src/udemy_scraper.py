#CONSTS
WEBSRC_PATHS = [ "../websource/1", "../websource/2", "../websource/3" ]
OUTPUT_PATH = "./output/"



import os
import warnings
import ex_questions
from lxml import etree



class Question:
    """ wrapper class for the question contents """

    def __init__(self, number, question, answers):
        self.number = number
        self.question = question
        self.answers = answers

    def __str__(self):
        return ",".join([ str(self.number), self.question, str(self.answers) ])




def parse_webpage(path_to_webpage):
    """ parse a webpage for its questions 

        Keyword arguments:
            path_to_webpage -- the path to the html file of the webpage

        returns:
            a list of questions
    """
    webpage = ""
    questions = []

    try:
        file = open(path_to_webpage, "r")
        webpage = file.read()
        file.close()
        webpage = etree.HTML(webpage)
        webpage = webpage.xpath("""//div[contains(@class, "detailed-result-panel--question-container")]""")

    except FileNotFoundError:
        warnings.warn("No file for " + path_to_webpage)


    if len(webpage) > 0:
        for question in webpage:

            __num = question.xpath(""".//span""")
            __question = question.xpath(""".//div[contains(@id, "question-prompt")]""")
            __answers = question.xpath(""".//div[contains(@class, "mc-quiz-answer--answer-inner")]""")

            for x in range(len(__answers)):
                __answers[x] = ( __answers[x][0].text, len(__answers[x]) == 2)

            if min([len(__num), len(__question), len(__answers)]) > 0:
                questions.append(Question(__num[0].text, __question[0].text, __answers))

    return questions






if __name__ == "__main__":
    """ writes every question from ./websource into files """
    
    for path in WEBSRC_PATHS:
        par_dir = path.split("/")[-1] if len(path.split("/")[-1]) > 0 else path.split("/")[-2]
        os.makedirs(OUTPUT_PATH + par_dir, exist_ok=True)

        #x = 0
        for file_name in list(filter(lambda file_name: file_name.endswith(".html"), os.listdir(path))):

            print("Converting: ", file_name)

            questions = parse_webpage(path + "/" + file_name)
            #for i in range(len(questions)): questions[i].number = x = x+1
            ex_questions.to_Gift(questions, OUTPUT_PATH + par_dir + "/" + file_name)

            print("Translating: ",file_name)

            questions_ger = ex_questions.trans_questions(questions)
            ex_questions.to_Gift(questions_ger, OUTPUT_PATH + par_dir + "/GER_" + file_name)

