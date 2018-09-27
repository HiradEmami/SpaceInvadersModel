# Required Imports
import os,time
from game import *
from interuption_generator import *
from eyetracker import Eyetracker
from clustering import Classifier
# Main Directories
DIFFICULTY_FOLDER = "difficulty_blocks"
PRIMARY_FOLDER = "system_info/"



def create_essentials():
    # if the primary path of blocks does not exist create a new folder
    if not os.path.exists(PRIMARY_FOLDER):
        print("creating The primary folder under " + PRIMARY_FOLDER)
        os.makedirs(PRIMARY_FOLDER)
        print(" The Folder for all saved information is created! \n The directory is : " + PRIMARY_FOLDER)
    else:
        print("Creating new Save File!")

    if not os.path.exists(PRIMARY_FOLDER + DIFFICULTY_FOLDER):
        print("creating The difficulty folder under " + PRIMARY_FOLDER + DIFFICULTY_FOLDER)
        os.makedirs(PRIMARY_FOLDER + DIFFICULTY_FOLDER)
        print(" The Folder for all saved difficulties is created! \n The directory is : "
              + PRIMARY_FOLDER + DIFFICULTY_FOLDER)
    else:
        print("Creating new Save File!")

def run_one_game_cycle(game,spawn_counter,interrupt = False):
    if not game.pause and not interrupt:
        spawn_counter += 1
        spawn_counter = game.performe_one_move_cycle(spawn_counter)
        time.sleep(game.frame_rate)
        game.main_frame.update()
    else:
        if interrupt:
            evaluation, root, evaluation_master = interrupt_user()
            root.destroy()
            evaluation_master.destroy()
        else:
         time.sleep(game.pause_duration_second)
        print("Resumed")
        game.after_pause_time = time.time()
        game.listen_for_action = True
        game.pause = False
        game.update_status_view()
    return game,spawn_counter

def interrupt_user():
    questions = [generate_question(), generate_question(), generate_question()]
    v = interuption(argQuestions=questions)
    result_of_test = v.ask_question_()
    #return  result_of_test
    return result_of_test

if __name__ == "__main__":
    eyeTracker = Eyetracker(1)
    eyeTracker.start()
    eyeTracker.disableGraphics()
    create_essentials()
    game = invaderGame()
    game.create_main_frame()

    # Primary while loop of the application
    spawn_counter = 0   # Spawn counter is used for the game to count the enemies
    game.game_state = "running" # running would start the game
    game.main_frame.update()    # Initial update of the main frame of the game, starts the game window
    # the main while loop
    while game.game_state == "running":
        #
        print eyeTracker.get_dilation()
        interrupt = False

        # run_one_game_cycle performance one cycle during which it checks the state of the game
        # if the state is running, the game is on the focus and is being played by the user
        # if the state is paused the game is halted for 5 seconds.
        # if the state is paused and the interrupt is set to true then the game is halted for the duration of\
        # the evaluation , during which a set of questions are asked and the state is evaluated before resuming the
        # game.
        game, spawn_counter = run_one_game_cycle(game=game, spawn_counter=spawn_counter,interrupt=interrupt )





