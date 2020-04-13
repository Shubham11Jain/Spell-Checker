""" import necessary libraries that are required for the spell checking """

from tkinter import * # for the GUI application
import numpy as np    # for Statistical operations
import time           # provides functions for working with times, and for converting between representations.
import json           # The JSON module is mainly used to convert the python dictionary above into 
                      # a JSON string that can be written into a file. 
from tkinter.messagebox import *

""" Making a class for the Spell checker """

class SpellChecker:
    
    def __init__(self):
        
        self.data = json.load(open("data.json")) #load the json file which is a database and which 
                                                 #contains almost all words in .json format file
        
        win = Tk()
        win.title("Spell Checker")  #title of the GUI interface
        win.geometry("400x400+500+200")     #size of the GUI interface (length x breadth)
        win.resizable(0,0)          #resizable is used to allow Tkinter root window to change 
                                    #it's size according to the users need as well we can prohibit resizing of the Tkinter window
        
        
        """ The following code includes the labelling, textboxes, buttons and their placing in the GUI interface """
        
        label1 = Label(text="Enter Your Word Here")
        label1.place(x=140,y=30)    #here, x and y are coordinates to where it should be placed
        self.txtbox1 = Entry(width=30)  #it allows user to write in the textbox
       # self.txtbox1.focus()
        self.txtbox1.place(x=105,y=60)
        check_btn = Button(text = "Check",fg='blue',width=10,command=self.check)  #this will create a button - "check" which carry out 
                                                                                 #the operation in the check function mentioned below
        check_btn.place(x=160,y=100)
        
        
        label2 = Label(text="Meaning/Suggestions")
        label2.place(x=20,y=150)    #here, x and y are coordinates to where it should be placed
        self.txt1 = Text(width=20,height=12,wrap=WORD)  #it allows user to write in the textbox
        self.txt1.place(x=15,y=180)
        
        label3 = Label(text="Add to Dictionary")
        label3.place(x=200,y=150)
        label4 = Label(text="Word")
        label4.place(x=200,y=180)
        self.txtbox2=Entry()    #it allows user to write in the textbox
        self.txtbox2.place(x=250,y=180)
        
        label5 = Label(text="Word Meaning")
        label5.place(x=200,y=200)
        self.txt2 = Text(width=21,height=7) #it allows user to write in the textbox
        self.txt2.place(x=200,y=230)
        add_btn = Button(text = "Add",fg='blue',width=10,command=self.add)    #this will create a button - "Add" which carry out 
                                                                        #the operation in the add function mentioned below
        add_btn.place(x=293,y=360)
        
        win.mainloop()
        
    #minimum edit distance algorithm    
    """
    Levenshtein Distance Algorithm is the minimum number of single-character
    edits required to change one word into the other.
    The operations include-> insertion, deletion, substitution.
    
    The levenshtein algorithm that finds the similar words if misspelled word is given as input
    """
    def levenshtein(self,seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))    #first to initialize the position
        for x in range(size_x):
            matrix [x, 0] = x       #initialize the distance array with position given for x.
        for y in range(size_y):
            matrix [0, y] = y       #initialize the distance array with position given for y.

    # So we repeatedly recompute the distance from initial case 
    #and by looking up the previously found ones, update its distance
    
        #Start from the initial state
        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:      #if the characters are same in both the strings
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1      #get the minimum edit distance from either string1 or string2 or both
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
    #     print (matrix)
        return (matrix[size_x - 1, size_y - 1]) #return the minimum edit distance between the characters of strings
    
    """this will show the suggested word if the user write the mispelled word  """    
    def suggestion(self):
        
        for i in self.data:
            if(self.levenshtein(self.txtbox1.get(),i)<=1):
                self.txt1.insert(END,i+"\n")
                
        
    """ Function to check if the given word is present in dictionary or not """
        
    def check(self):
        self.txt1.delete("1.0",END)     #delete if anything present in the textarea first
        
        if(self.txtbox1.get().lower() in self.data):
            self.txt1.insert(END,self.data[self.txtbox1.get().lower()][0])  #if the word is present in the dictionary,
                                                                            #then it will give the meaning of that particular word
        else:
            self.txt1.insert(END,"Word doesn't exist.\nSuggested Words:\n") #else, it shows the message that word doesn't exist and 
                                                                            #call the suggestion function to show some suggested words 
                                                                            #related to that word that the user was looking for
            self.suggestion()
    
    """ A simple function to add words to the dictionary """
        
    def add(self):
        if(self.txtbox2.get()!=None and self.txt2.get("1.0",END)!=None):
            if(self.txtbox2.get() not in self.data):  #if the word is not present in the dictionary, then it allows the user to add 
                                                        #that word and its meaning in the dictionary only for that particular operation, not permanent
                self.data[self.txtbox2.get()]=[self.txt2.get("1.0",END)]
                
                self.txtbox2.delete(0,END)      #clear the textarea of the label "word"   
                self.txt2.delete("1.0",END)     ##clear the textarea of the label "word meaning"
                self.txt2.insert(END,"Successfully Added")

                
            else:
                self.txt2.delete("1.0",END)     #else, it will show that the particular word is already present in the dictionary
                self.txt2.insert(END,"Word already present in dictionary")
                    
S1 = SpellChecker()