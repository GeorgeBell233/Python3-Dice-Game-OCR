#Client Requirements
#The players roll two 6-sided dice each and get points depending on what they
#roll. There are 5 rounds in a game. In each round, each player rolls the two dice.

# The rules are:
# • The points rolled on each player’s dice are added to their score.
# • If the total is an even number, an additional 10 points are added to their score.
# • If the total is an odd number, 5 points are subtracted from their score.
# • If they roll a double, they get to roll one extra die and get the number of points rolled added to their score.
# • The score of a player cannot go below 0 at any point.
# • The person with the highest score at the end of the 5 rounds wins.
# • If both players have the same score at the end of the 5 rounds, they each roll 1 die and whoever gets the highest score wins (this repeats until someone wins).

# Only authorised players are allowed to play the game.
# Where appropriate, input from the user should be validated.

# Design, develop, test and evaluate a program that:

# 1. Allows two players to enter their details, which are then authenticated to ensure that they are
# authorised players.
# 2. Allows each player to roll two 6-sided dice.
# 3. Calculates and outputs the points for each round and each player’s total score.
# 4. Allows the players to play 5 rounds.
# 5. If both players have the same score after 5 rounds, allows each player to roll 1 die each until someone wins.
# 6. Outputs who has won at the end of the 5 rounds.
# 7. Stores the winner’s score, and their name, in an external file.
# 8. Displays the score and player name of the top 5 winning scores from the external file

# Importing Modules
import random as r #Imports random to roll dice
import hashlib #Imports hashlib for hashing the password
import os #Imports os for os.path.join and os.urandom
import sys #Imports sys for sys.path[0] to help find files within current directory
import csv #Imports csv to handle csv files
import time #Imports time to delay clearing
import getpass #Used to enter password without showing
import platform
from typing import Type #Used to identify OS

def clear():
        if "idlelib" in sys.modules:
            for i in range(0,100):
                print("\n")
        else:
            if platform.system() == "Windows": 
                os.system("cls") 
            elif platform.system() == "Linux" or "Darwin": #Darwin is Mac OS
                os.system("clear")

def getpassVsInput(Text):
        if "idlelib" in sys.modules:
            Value = input(Text)
        else:
            Value = getpass.getpass(Text)
        return Value

# Authentication Functions
def Sha512Hash(Password, salt):  # Uses the password and the salt to create the hash
    HashedPassword = hashlib.pbkdf2_hmac('sha512',Password.encode('utf-8'),salt,100000) #Encodes the password and salt to utf-8, automatic hexdigest
    return HashedPassword

def DuplicateUserCheck(P1Name,P2Name):
    if P1Name != "" and P1Name == P2Name:  # Checks that P1 Name is assigned and if it has, that the usernames are not the same, to prevent duplicate logins
        return True
    else:
            return False

def LoginSystem(P1Name,UsernameSaltandHash): #Input is list containing the Username, salt and hash information
    print("-----Login System-----")

    Name = input("Enter a username ") #Login name and password info is inputted by user
    Password = getpassVsInput("Enter a password, it will not echo your input if ran with a terminal (such as visual studio code) ")

    if DuplicateUserCheck(P1Name,Name): #Checks if the username is duplicate, if so it does not compare it to the list
        print("Duplicate User, use different login \n")
        return "" #return "" shows that the login has failed
    else:
        for i in range(0,len(UsernameSaltandHash)): #Runs code for each sub-list within the 2d array
            if Name == UsernameSaltandHash[i][0] and str(Sha512Hash(Password, bytes.fromhex(UsernameSaltandHash[i][1]))) == UsernameSaltandHash[i][2]:
            #Checks if the username within the current value of i is the same as the inputted name and 
            #if the password inputted, after being salted and hashed is the same to the previously salted and hashed password stored for that Username
                    print("Successful Login to", Name,"\n")
                    time.sleep(1.5)
                    clear()
                    return Name
            elif i == len(UsernameSaltandHash)-1: #If all of the name checks fails, then the login fails
                print("Login failed, please try again \n")
                time.sleep(1.5)
                clear()
                return ""

# Dice Functions
def SinglePlayerDiceCycle(Score):  # Used for each players dice cycle that is iterated 5 times
    # Rolling two dice
    DiceRoll = []
    for _ in range(0, 2):
        DiceRoll.append(r.randint(1, 6))
    
    # Adds sum of dice rolls to score
    Score += sum(DiceRoll)

    # Checks for odd/even number and either -5 or +10
    if sum(DiceRoll) % 2 == 0:  # Divides the sum of the dice rolls by 2, and if there are any remainders left
        Score += 10
    else:
        if Score-5 < 0:  # Checks to see if subtracting 5 would cause the score to go under 0, if so the score will be
            # set to 0, otherwise 5 will be subtracted from the score
            Score = 0
        else:
            Score += -5

    # Checks for doubles, and acts accordingly
    if DiceRoll[0] == DiceRoll[1]:
        Score += r.randint(1,6)

    return Score

# External File Functions

def Quicksort (Sequence):
    #Lists to append to
    SmallerThanPivot = []
    SameAsPivot = []
    LargerThanPivot = []
    
    if len(Sequence) <= 1: #If true this section of the quicksort should not be recursive any longer
        return(Sequence)
    else:
        pivot = Sequence.pop(r.randint(0,len(Sequence)-1)) #Creates a random pivot to help avoid worse case big-o-notation for already sorted lists

        for i in range(0,len(Sequence)): 
            if int(Sequence[i][1]) > int(pivot[1]):
                LargerThanPivot.append(Sequence[i])
            elif int(Sequence[i][1]) == int(pivot[1]):
                SameAsPivot.append(Sequence[i])
            else:
                SmallerThanPivot.append(Sequence[i])
        
        return (Quicksort(LargerThanPivot) + SameAsPivot + [pivot] + Quicksort(SmallerThanPivot)) #Starts recursion on the lists containing values larger or smaller than the pivot


def CSVFileWriter(WinnerName,WinnerScore):
    UserRow=[WinnerName,WinnerScore] #Combines WinnerName and Winner Score into a list
    try:
        with open (os.path.join(sys.path[0],"ScoresAndUsernames"),"a", newline = "") as Scoreboard: #Tries to open and append UserRow to a CSV file
            writer = csv.writer(Scoreboard)
            writer.writerow(UserRow)
    except FileNotFoundError:
        with open (os.path.join(sys.path[0],"ScoresAndUsernames"),"w") as Scoreboard: #If the File is not found, the file is created and UserRow is written to it
            writer = csv.writer(Scoreboard)
            writer.writerow(UserRow)

def CSVTo2DArray(Directory):
    TwoDArray=[] #Creates 2D array for CVS file to be added to
    
    try:
        with open(os.path.join(sys.path[0],Directory),"r") as file: #Opens file in specified directory
            reader = csv.reader(file)
            for row in reader: #Repeats for the number of rows within the CSV File
                TwoDArray.append(row)
        
        return TwoDArray
    
    except FileNotFoundError:
        return []

#Scoreboard printing
def ScoreboardScrolling(ScoreboardPosition,Three_d_Scoreboard): #Function to be used only within function ScoreboardAndScroll
        print("<---Back  " + "Page", ScoreboardPosition+1,"of",len(Three_d_Scoreboard)," Next--->")
        
        ScoreboardSelection = input("Enter next or forward to see the next page, Enter back or previous to see the previous page, Enter a number to go to that page ")
        
        #Uses ScoreboardSelection input to either increment the scoreboard forward or backwards
        try:
            ScoreboardSelection = int(ScoreboardSelection)
            
            if ScoreboardSelection <= len(Three_d_Scoreboard):
                ScoreboardPosition = ScoreboardSelection-1
            else:
                print("The number is too high")

        except ValueError:
            if ScoreboardSelection.lower() in ["back","previous"]:
                if ScoreboardPosition - 1 < 0: #Ensures the index never goes below 0
                    print("No previous scores")
                    time.sleep(1.5)
                else:
                    ScoreboardPosition -= 1 
            
            elif ScoreboardSelection.lower() in ["next","forward"]:
                if ScoreboardPosition + 1 >= len(Three_d_Scoreboard): #Ensures the index never goes above maximum in list
                    print("No further scores")
                    time.sleep(1.5)
                else:
                    ScoreboardPosition +=1
            
            else:
                print("Unrecognised input")
                time.sleep(1.5)
    
        clear()    
        return [ScoreboardPosition,ScoreboardSelection]

def ScoreboardAndScroll(WinnerName,WinnerScore,LoserName,LoserScore):
    Scoreboard = CSVTo2DArray("ScoresAndUsernames") #Turns csv file into 2d arrays
    Scoreboard = Quicksort(Scoreboard) #Sorts Unsorted scoreboard using sorting algorithm (Quicksort)
    Three_d_Scoreboard = []
    
    while Scoreboard != []: #Turns 2d array of Scoreboard into 3-d array with the initial sub-array's containing 5 or less scores each
        TempArray = [] #Temp array is used to store 5 array and is appeneded to Three_d_scoreboard with the function
        
        if len(Scoreboard) >= 5:
            for _ in range(0,5): #_ used to indicate the variable is not used
                TempArray.append(Scoreboard.pop(0))
        
        elif len(Scoreboard) != 0: #_ used to indicate the variable is not used
            for _ in range(0,len(Scoreboard)):
                TempArray.append(Scoreboard.pop(0))
        
        Three_d_Scoreboard.append(TempArray)

    ScorePosition = int(0)
    Exit = False

    while Exit == False: 
        print("-----Scores-----") #Used for better appearance
        print(WinnerName, "wins with a score of", WinnerScore)
        print(LoserName, "lost with a score of", LoserScore)
                
        print("-----Scoreboard-----")
        
        if len(Three_d_Scoreboard[ScorePosition]) < 5: #If there are less than 5 records, it prints all scores and usernames within the list
            for i in range(0,len(Three_d_Scoreboard[ScorePosition])): #Goes through all indexs in the array
                print(str((ScorePosition*5) + (i+1)) + ") " + Three_d_Scoreboard[ScorePosition][i][0] + " : " + Three_d_Scoreboard[ScorePosition][i][1])
                
                #str((ScorePosition*5) + (i+1)) + ") calculates which datapoint it is, by multplying Scoreposition by 5, then adding one to the current index
                #The rest prints a bracket, the Name, a colon and then the score
            
            Output = ScoreboardScrolling(ScorePosition,Three_d_Scoreboard)
            ScorePosition = Output[0]

            try:
                if Output[1].lower() in ["exit","finish","end"]:
                    Exit = True
            except AttributeError:
                Exit = False

        else: #If there are more than 5 records, it prints the first 5 usernames and scores, which are already in order
            for i in range(0,5):
                print(str((ScorePosition*5) + (i+1)) + ") " + Three_d_Scoreboard[ScorePosition][i][0] + " : " + Three_d_Scoreboard[ScorePosition][i][1])
            #str((ScorePosition*5) + (i+1)) + ") calculates which datapoint it is, by multplying Scoreposition by 5, then adding one to the current index
            #The rest prints a bracket, the Name, a colon and then the score
            
            Output = ScoreboardScrolling(ScorePosition,Three_d_Scoreboard)
            ScorePosition = Output[0]

            try:
                if Output[1].lower() in ["exit","finish","end"]:
                    Exit = True
            except AttributeError:
                Exit = False

# Authentication Code/Setup
# Sets names to empty strings
P1Name = ""
P2Name = ""

# List containing Usernames,Salt and hashed password
UsernameSaltHashedPassword = CSVTo2DArray("UsernameSaltHashedPassword")
if len(UsernameSaltHashedPassword)<2:
    print("Unable to login/play due to not enough login's being provided")
    raise SystemExit

# Ensures P1 has a set name
while P1Name in [""]:
    P1Name = LoginSystem(P1Name,UsernameSaltHashedPassword)
# Ensures P2 has a set name
while P2Name in [""]:
    P2Name = LoginSystem(P1Name,UsernameSaltHashedPassword)

# Dice Code/Setup
# Sets up score tracker
P1Score = int(0)
P2Score = int(0)

for i in range(0, 5):  # 5 Dice Cycles for each player
    P1Score = SinglePlayerDiceCycle(P1Score)
    P2Score = SinglePlayerDiceCycle(P2Score)

while P1Score == P2Score:  # Checks for draw and each player rolls dice until it there is a winner
    P1Score += r.randint(1, 6)
    P2Score += r.randint(1, 6)
    print(P1Score, P2Score)

# Checks who is winner
if P1Score > P2Score:
        CSVFileWriter(P1Name,P1Score) #Writes to a CSV file the new username and score
        ScoreboardAndScroll(P1Name,P1Score,P2Name,P2Score) #Shows the top 5 scores and the respective usernames
else:
        CSVFileWriter(P2Name,P2Score) #Writes to a CSV file the new username and score
        ScoreboardAndScroll(P2Name,P2Score,P1Name,P1Score) #Shows the top 5 scores and the respective usernames

clear()
