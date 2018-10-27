# Required Imports
import os,time
import random
from game import *
from interuption_generator import *
from eyetracker import Eyetracker
from clustering import Classifier
import numpy as np
import sys



# Main Directories
PRIMARY_FOLDER = "Final_result_spaceInvader/"

min_duration_between_interruption = 30 #seconds
Interruption_timmer = 0
interruption_allowed = False

evaluation_list = []

def create_essentials(partName):
    # if the primary path of blocks does not exist create a new folder
    if not os.path.exists(PRIMARY_FOLDER):
        print("creating The primary folder under " + PRIMARY_FOLDER)
        os.makedirs(PRIMARY_FOLDER)
        print(" The Folder for all saved information is created! \n The directory is : " + PRIMARY_FOLDER)
    else:
        print("Creating new Save File!")
    partName=str(partName)+"/"
    if not os.path.exists(PRIMARY_FOLDER + partName):
        print("creating The difficulty folder under " + PRIMARY_FOLDER + partName)
        os.makedirs(PRIMARY_FOLDER + partName)
        print(" The Folder for all saved difficulties is created! \n The directory is : "
              + PRIMARY_FOLDER + partName)
    else:
        print("Creating new Save File!")
    return  PRIMARY_FOLDER + partName
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
            evaluation_list.append([evaluation,game.get_current_stage_difficulty(), game.interruption_state])
            print(game.get_current_stage_difficulty(), game.interruption_state)
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
    global Interruption_timmer
    global interruption_allowed
    questions = [generate_question(), generate_question(), generate_question()]
    v = interuption(argQuestions=questions)
    result_of_test = v.ask_question_()
    Interruption_timmer = time.time()
    interruption_allowed = False
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
    global Interruption_timmer
    global interruption_allowed

    game = invaderGame(False)
    game.create_main_frame()
    # Primary while loop of the application
    spawn_counter = 0   # Spawn counter is used for the game to count the enemies
    game.game_state = "running" # running would start the game
    game.main_frame.update()    # Initial update of the main frame of the game, starts the game window
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
        if current_time - (Interruption_timmer) > min_duration_between_interruption:
            interruption_allowed = True
            print(Interruption_timmer)

        else:
            interruption_allowed = False

        #get the current workload and check if the workload is low
        workload, listlength = classifier.getResult()
        try:
           # if random.randint(0,100) < 5:
           #     interrupt = True
           if (workload <= (1/listlength)) and (game.interruption_state == "IMS") and interruption_allowed == True:
              print ('Good moment for interruption')
              interrupt = True
           elif (game.interruption_state == "Random")and interruption_allowed == True:
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
        interrupt = False

    return game, logData
if __name__ == "__main__":
    Participant_name= sys.argv[1]
    result_folder= create_essentials(partName=Participant_name)
    eyeTracker = Eyetracker(1)
    eyeTracker.start()
    eyeTracker.disableGraphics()

	
    initData = run_trial()
    np.savetxt(result_folder+'initData.csv', initData, fmt = '%s')
    print(len(initData))
    classifier = Classifier(initData)
    game,logData = run_condition(classifier)

    np.savetxt(result_folder + "logData.csv", logData, fmt='%s')
    #the final stuffs for response time and the list for evaluation of the interruption
    response_list = game.response_recordings
    game.__del__()
    print ("response times",response_list)
    np.savetxt(result_folder+'responseList.csv', response_list, fmt = '%s')
    np.savetxt( result_folder+ 'evaluationList.csv', evaluation_list, fmt = '%s')
    print ("evaluations",evaluation_list)



