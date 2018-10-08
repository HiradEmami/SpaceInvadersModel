# Required Imports
import os,time
import random
from game import *
from interuption_generator import *
from eyetracker import Eyetracker
from clustering import Classifier
import numpy as np


# Main Directories
DIFFICULTY_FOLDER = "difficulty_blocks"
PRIMARY_FOLDER = "system_info/"

Interruption_timmer = 0

evaluation_list = []

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
            evaluation_list.append(evaluation)
            game.listen_for_action = True
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
    Interruption_timmer = time.time()
    #return  result_of_test
    return result_of_test

def run_trial():
    initialData = []
    trial_game = invaderGame(argTrial=TRIAL)
    trial_game.create_main_frame()
    spawn_counter = 0
    trial_game.game_state = "running"
    trial_game.main_frame.update()
    while trial_game.game_state == "running":
	
        if not trial_game.pause:
            dilation = eyeTracker.get_dilation()
            try:
                if dilation is not None:
                    initialData.append(dilation)
            except:
               print ('exeption thrown')
            spawn_counter += 1
            spawn_counter = trial_game.performe_one_move_cycle(spawn_counter)
            time.sleep(trial_game.frame_rate)
            trial_game.main_frame.update()
        else:
            time.sleep(trial_game.pause_duration_second)
            print("Resumed")
            trial_game.after_pause_time = time.time()
            trial_game.listen_for_action = True
            trial_game.pause = False
            trial_game.update_status_view()
    trial_game.__del__()
    return initialData





def run_condition(classifier):
    game = invaderGame(False)
    game.create_main_frame()
    # Primary while loop of the application
    spawn_counter = 0   # Spawn counter is used for the game to count the enemies
    game.game_state = "running" # running would start the game
    game.main_frame.update()    # Initial update of the main frame of the game, starts the game window
    min_interrupt_time = 25   #minimum # of seconds between interruptions
    logData = []

    Interruption_timmer = time.time()
    interruption_allowed = False

    # the main while loop
    while game.game_state == "running":
        dilation = eyeTracker.get_dilation()
        if dilation is not None:
           label, mean = classifier.update(dilation)
           logData.append((dilation, label, classifier.protos[0], classifier.protos[1], game.get_current_stage_difficulty(), game.interruption_state))
           sum, N = classifier.getResult()
           print sum, N
        #logData.append(dilation)

        # Setting the interruption to false by default
        interrupt = False

        #the timer for interruption
        current_time = time.time()

        if current_time - Interruption_timmer > 30:
            interruption_allowed = True


        #get the current workload and check if the workload is low
        workload, listlength = classifier.getResult()
        try:
           if (workload <= (1/listlength)) and (game.interruption_state == "IMS") and (time.time() >= (game.after_pause_time + min_interrupt_time)):
              print ('Good moment for interruption')
              interrupt = True
           elif (game.interruption_state == "Random") and (time.time() >= (game.after_pause_time + min_interrupt_time + random.randint(-10,10))):
              interrupt = True
        except:
           print ('exception interrupt detection')

        # run_one_game_cycle performance one cycle during which it checks the state of the game
        # if the state is running, the game is on the focus and is being played by the user
        # if the state is paused the game is halted for 5 seconds.
        # if the state is paused and the interrupt is set to true then the game is halted for the duration of\
        # the evaluation , during which a set of questions are asked and the state is evaluated before resuming the
        # game.
        game, spawn_counter = run_one_game_cycle(game=game, spawn_counter=spawn_counter,interrupt=interrupt )
    np.savetxt("logData.csv", logData, fmt = '%s')
    return game
if __name__ == "__main__":
   
    eyeTracker = Eyetracker(1)
    eyeTracker.start()
    eyeTracker.disableGraphics()
    create_essentials()
	
    initData = run_trial()
    np.savetxt('initData.csv', initData, fmt = '%s')
    print(len(initData))
    classifier = Classifier(initData)
    game = run_condition(classifier)
    response_list = game.response_recordings
    game.__del__()
    print ("response times",response_list)
    print ("evaluations",evaluation_list)



