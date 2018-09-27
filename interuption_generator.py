from tkinter import *
import random as rd


__author__ = 'Hirad Emami Alagha - s3218139'
#   Question Format = (a,b,operation)
class interuption():
    def __init__(self,argQuestions):
        # Message Box Elements
        self.entry1 = None
        self.entry2 = None
        self.entry3 = None
        self.res1 = None
        self.res2 = None
        self.res3 = None
        self.root = None
        self.complete_button = None
        # Question Progression
        self.first_Question = False
        self.second_Question = False
        self.third_Question = False
        # Questions
        self.questions = argQuestions
        # Evaluation
        self.evaluation = None
        self.evaluation_master = None



    def find_answer(self,a,b,operation):
        if operation == "addition":
            return  a + b
        elif operation == "subtraction":
            return  a - b
        elif operation == "multiplication":
            return  a * b
        elif operation == "division":
            return a / b

    def get_operation_symbol(self,operation):
        if operation == "addition":
            return  " + "
        elif operation == "subtraction":
            return  " - "
        elif operation == "multiplication":
            return  " x "
        elif operation == "division":
            return " / "

    def evaluate_question1_function(self,event):
        value = int(self.entry1.get())
        answer= int(self.find_answer(self.questions[0][0],self.questions[0][1],self.questions[0][2]))
        if value == answer:
            result = 'correct'
            self.first_Question = True
            self.entry2.focus()
        else:
            result = 'incorrect'
            self.first_Question = False
        self.res1.configure(text="Your Answer is : " +result )

    def evaluate_question2_function(self,event):
        if not self.first_Question:
            self.res2.configure(text="Answer the First Question")
        else:
            value = int(self.entry2.get())
            answer = int(self.find_answer(self.questions[1][0], self.questions[1][1], self.questions[1][2]))
            if value == answer:
                result = 'correct'
                self.second_Question = True
                self.entry3.focus()
            else:
                result = 'incorrect'
                self.second_Question = False
            self.res2.configure(text="Your Answer is : " + result)

    def evaluate_question3_function(self,event):
        if not self.second_Question:
            self.res3.configure(text="Answer the First Question" )
        else:
            value = int(self.entry3.get())
            answer = int(self.find_answer(self.questions[2][0], self.questions[2][1], self.questions[2][2]))
            if value == answer:
                result = 'correct'
                self.third_Question = True
                self.complete_button.focus()
            else:
                result = 'incorrect'
                self.third_Question = False
            self.res3.configure(text="Your Answer is : " + result)


    def finish_question(self):
        if self.third_Question:
            self.root.quit()
            self.ask_evaluation()
        else:
            print("Not Completed")

    def happy_button(self):
        self.evaluation = 'happy'
        self.evaluation_master.quit()

    def sad_button(self):
        self.evaluation = 'sad'
        self.evaluation_master.quit()

    def angry_button(self):
        self.evaluation = 'angry'
        self.evaluation_master.quit()

    def ask_evaluation(self):
        self.evaluation_master = Tk()
        self.evaluation_master.title('Evaluation')
        self.evaluation_master.geometry("200x200")  # You want the size of the app to be 500x500
        self.evaluation_master.resizable(0, 0)

        self.photo_a = PhotoImage(file="spaceShip/happy.gif",master=self.evaluation_master)
        self.photo_b = PhotoImage(file="spaceShip/sad.gif",master=self.evaluation_master)
        self.photo_c = PhotoImage(file="spaceShip/angry.gif",master=self.evaluation_master)

        a = Button(self.evaluation_master,image=self.photo_a, text="it was fine!", command=self.happy_button,
                   height=50,width=150, compound=LEFT)
        b = Button(self.evaluation_master, image=self.photo_b,text="didn't like it!", command=self.sad_button,
                   height=50, width=150, compound=LEFT)
        c = Button(self.evaluation_master, image=self.photo_c,text="Made me angry!", command=self.angry_button,
                   height=50, width=150, compound=LEFT)

        w = Label(self.evaluation_master, text="How was the interruption? ")

        w.pack()
        a.pack()
        b.pack()
        c.pack()

        mainloop()



    def ask_question_(self):
        self.root = Tk()
        self.root.title('The game')
        # You can set the geometry attribute to change the root windows size
        self.root.geometry("250x250")  # You want the size of the app to be 500x500
        self.root.resizable(0, 0)

        q1 = str(self.questions[0][0])+str(self.get_operation_symbol(self.questions[0][2]))+\
             str(self.questions[0][1])+" = ?"
        Label(self.root, text=q1).pack()
        self.entry1 = Entry(self.root)
        self.entry1.bind("<Return>", self.evaluate_question1_function)
        self.entry1.pack()
        self.res1 = Label(self.root)
        self.res1.pack()
        # set focus to entry 1
        self.entry1.focus()

        q2 = str(self.questions[1][0]) + str(self.get_operation_symbol(self.questions[1][2])) +\
             str(self.questions[1][1]) + " = ?"
        Label(self.root, text=q2).pack()
        self.entry2 = Entry(self.root)
        self.entry2.bind("<Return>", self.evaluate_question2_function)
        self.entry2.pack()
        self.res2 = Label(self.root)
        self.res2.pack()

        q3 = str(self.questions[2][0]) + str(self.get_operation_symbol(self.questions[2][2])) + \
             str(self.questions[2][1]) + " = ?"
        Label(self.root, text=q3).pack()
        self.entry3 = Entry(self.root)
        self.entry3.bind("<Return>", self.evaluate_question3_function)
        self.entry3.pack()
        self.res3 = Label(self.root)
        self.res3.pack()
        self.complete_button = Button(self.root, text='Complete the test!',
                    command=self.finish_question)
        self.complete_button.pack()
        self.root.mainloop()

        return self.evaluation ,self.root ,self.evaluation_master


def generate_question():
    operations = ["addition","multiplication","subtraction","division"]
    selected = operations[rd.randint(0,len(operations)-1)]
    if selected == "division":
        found = False
        while not found:
            a = rd.randint(10,100)
            b = rd.randint(1,10)
            if a % b == 0:
                found = True
                return (a,b,selected)
    elif selected == "multiplication":
        return (rd.randint(0, 10), rd.randint(0, 10), selected)
    else:
        return (rd.randint(0,50) , rd.randint(0,50) , selected)



if __name__ == "__main__":
    dummy_questions = [generate_question(),generate_question(),generate_question()]
    v = interuption(argQuestions=dummy_questions)
    result_of_test =v.ask_question_()
    print(result_of_test)