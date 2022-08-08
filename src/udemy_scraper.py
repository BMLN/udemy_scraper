import os
import ex_questions
from argparse import ArgumentParser
from lxml import etree


#"CONSTS"
WEBSRCS = [ str(y[0]) + "/" + str(x) for y in os.walk("../websource") for x in y[2] ]
OUTPUT_PATH = "../output"




#DEFS
class Question:
    """ wrapper class for the question contents """

    def __init__(self, number, question, answers):
        self.number = number
        self.question = question
        self.answers = answers

    def __str__(self):
        return ",".join([ str(self.number), str(self.question), str(self.answers) ])




def parse_webpage(path_to_webpage):
    """ parse a webpage for its questions 

        Keyword arguments:
            path_to_webpage -- the path to the html file of the webpage

        returns:
            a list of questions
    """
    webpage = "default"
    questions = []

    try:
        file = open(path_to_webpage, "r")
        webpage = file.read()
        file.close()

    except FileNotFoundError:
        print("Warning:", "No file for", path_to_webpage)

    webpage = etree.HTML(webpage)
    webpage = webpage.xpath("""//div[contains(@class, "detailed-result-panel--question-container")]""")

    for question in webpage:

        __num = question.xpath(""".//span""")
        __question = question.xpath(""".//div[contains(@id, "question-prompt")]""")
        __answers = question.xpath(""".//div[contains(@class, "mc-quiz-answer--answer-inner")]""")

        for x in range(len(__answers)):
            __answers[x] = ( __answers[x][0].text, len(__answers[x]) == 2)

        if min([len(__num), len(__question), len(__answers)]) > 0:
            questions.append(Question(__num[0].text, __question[0].text, __answers))

    return questions


all_questions = []

def is_contained(question):
    if question.question not in (quest.question for quest in all_questions):
        all_questions.append(question)
        return question
    else:
        #print('Question '+question.number+' is double, will be deleted')
        return None 

def filter_questions(questions):
    return list(filter(lambda question: is_contained(question), questions))



#PROG
if __name__ == "__main__":
    """ writes every question from ./websource into files """
    count_doubled = 0
    
    arg_parser = ArgumentParser(description="writes questions from udemy websources into files")
    arg_parser.add_argument("--src", type=str, nargs="+", help="all the source files", default=WEBSRCS)
    arg_parser.add_argument("--dest", type=str, help="the destination folder for the generated files", default=OUTPUT_PATH)
    args = arg_parser.parse_args()


    #x = 0
    for src_file in list(filter(lambda file_name: file_name.endswith(".html"), args.src)):
        
        par_dir = src_file.split("/")[-2] if "/" in src_file else "./"
        file_name = src_file.split("/")[-1] if "/" in src_file else src_file
        os.makedirs(os.path.join(OUTPUT_PATH, par_dir), exist_ok=True)

        print("Converting: ", file_name)
        
        questions = parse_webpage(src_file)
        questions_filtered = filter_questions(questions)
        count_doubled += len(questions) - len(questions_filtered)
        #for i in range(len(questions)): questions[i].number = x = x+1
        ex_questions.to_Gift(questions_filtered, OUTPUT_PATH + "/" + par_dir + "/" + file_name)

        ## TRANSLATION ##
        #print("Translating: ",file_name)
        #questions_ger = ex_questions.trans_questions(questions_filtered)
        #ex_questions.to_Gift(questions_ger, OUTPUT_PATH + par_dir + "/GER_" + file_name)

    print('Deleted '+str(count_doubled)+' questions because they were doubled.')

