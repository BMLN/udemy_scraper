#CONSTS
WEBSRC_PATHS = [ "./websource/" ]




import os
import warnings
from lxml import etree



class Question:
    """ wrapper class for the question contents """

    def __init__(self, number, question, answers):
        self.number = number
        self.question = question
        self.answers = answers

    def __str__(self):
        return ",".join([ self.number, self.question, str(self.answers) ])




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

            if min([len(__num), len(__question), len(__answers)]) >= 1:
                questions.append(Question(__num[0].text, __question[0].text, __answers))

    return questions






if __name__ == "__main__":
    questions = []

    for path in WEBSRC_PATHS:
        for file_name in list(filter(lambda file_name: file_name.endswith(".html"), os.listdir(path))):
            #questions += parse_webpage(path + "/" + file_name)
            questions += parse_webpage("C_TS410_1909 & 2020 dumps SAP Business Process Integration _ Udemy.html")

    #for x in questions:
        #print(x)