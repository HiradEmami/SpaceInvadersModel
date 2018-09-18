# Required Imports
import os
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



if __name__ == "__main__":
    create_essentials()