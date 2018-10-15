from interuption_generator import *
import time

def interrupt_user():
    questions = [generate_question(), generate_question(), generate_question()]
    v = interuption(argQuestions=questions)
    result_of_test = v.ask_question_()
    Interruption_timmer = time.time()
    #return  result_of_test
    return result_of_test



i = 0

for k in range(100):
    k+=1
    if k==98:
        interrupt_user()
    print (k)
