# Required Imports
import os,time
from game import *
from interuption_generator import *
import threading
from threading import Thread
from multiprocessing import Process

# Main Parameters
DIFFICULTY_FOLDER = "difficulty_blocks"


def create_essentials():
    # if the primary path of blocks does not exist create a new folder
    if not os.path.exists(DIFFICULTY_FOLDER):
        print("creating The primary folder under " + DIFFICULTY_FOLDER)
        os.makedirs(DIFFICULTY_FOLDER)
        print(" The Folder for all saved worlds is created! \n The directory is : " + DIFFICULTY_FOLDER)
    else:
        print("Creating new Save File!")


def run_game():
    game = invaderGame()
    game.run()

def intrupt_user():
    questions = [generate_question(), generate_question(), generate_question()]
    v = interuption(argQuestions=dummy_questions)
    result_of_test = v.ask_question_()
    print(result_of_test)
    #return  result_of_test

if __name__ == "__main__":
    create_essentials()
    run_game()



