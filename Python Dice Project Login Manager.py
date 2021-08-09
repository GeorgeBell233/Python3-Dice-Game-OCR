import os #Imports os for os.urandom and os.path.join
import hashlib #Imports hashlib for hashing with sha512
import sys #Imports sys for sys.path[0] which allows the program to know the directory the python file is stored in
import csv #Imports csv to handle csv files
import getpass #Imports getpass to not echo password
import platform #Imports platform to identify OS

def SaltGenerator():  # Used to generate Salts to be stored, will not be run in final code as salts will be stored
    salt = os.urandom(64)  # Generates a cryptographically secure random string
    return salt

def Sha512Hash(Password, salt):  # Uses the password and the salt to create the hash
    HashedPassword = (hashlib.pbkdf2_hmac('sha512',Password.encode('utf-8'),salt,100000))
    #Encodes the password and salt to utf-8, automatic hexdigest
    return HashedPassword

def CSVFileReader(Directory):
    try:  # Tries to open the file, if the FileNotFound exception is the file is created
        with open (os.path.join(sys.path[0],Directory),"r") as File:
            reader = csv.reader(File)  # If the file opening is successful the file is read
            UsernameSaltHashedPassword = list(reader) #Coverts UsernameSaltHashed password into a list
    except FileNotFoundError:
        with open (os.path.join(sys.path[0],Directory),"w") as File:
            print("File was not found, it has now been created")  # If the file is not found, it is created
            UsernameSaltHashedPassword = []
    
    return(UsernameSaltHashedPassword)

def CSVWrite(Directory,Value):
    with open (os.path.join(sys.path[0],Directory),"w", newline = "") as Write: #Opens file in current directory,
        #which has already been created previously if it was not already present
        writer = csv.writer(Write) #Creates csv.writer
        for items in Value: #Iterates through all values in the list
            writer.writerow(items) #Writes the content of Value to a new row in the CSV File

def clear():
        if "idlelib" in sys.modules:
            for i in range(0,100):
                print("\n")
        else:
            if platform.system() == "Windows": #Darwin is Mac OS, Linux is any linux distribution and Windows is windows
                os.system("cls") 
            elif platform.system() == "Linux" or "Darwin":
                os.system("clear")

def getpassVsInput(Text):
        if "idlelib" in sys.modules:
            Value = input(Text)
        else:
            Value = getpass.getpass(Text)
        
        return Value

UsernameSaltHashedPassword = CSVFileReader("UsernameSaltHashedPassword")

#Creates a list of Usernames already present within the file
UsernamesInUse = []
for Values in UsernameSaltHashedPassword: #Iterates through all index's in the list
    UsernamesInUse.append(Values[0])

#Repeats until valid input is recieved, if invalid input is entered the input returns None
NoOfSequences = None
while NoOfSequences == None:
    try:
        print("There are " + str(len(UsernamesInUse)) + " login/s already set up.")
        NoOfSequences = int(input("How many logins do you want to add, if there are less than 2 logins it will repeat until there are at least 2. "))
    except:
        print("Invalid Input, please try again")
#Ensures 2 logins will be made by changing the NoOfSequences if not enough logins will be added      

if len(UsernameSaltHashedPassword) == 0 and NoOfSequences in [0,1]:
    NoOfSequences = 2
    print("The number of logins to be added will be 2 as there are not enough logins. There are currently ",len(UsernamesInUse)," logins already set")
elif len(UsernameSaltHashedPassword) == 1 and NoOfSequences in [0]:
    print("The number of logins to be added will be 2 as there are not enough logins")
    NoOfSequences = 1

UsernameSaltHashedPassword = CSVFileReader("UsernameSaltHashedPassword") #Opens file and converts to 2D array, or creates list if file was not found

for i in range(0, NoOfSequences):
    #Creates a 2D array with each sub-list containing a Username Salt and HashedPassword
    UsernameDuplicate = True

    while UsernameDuplicate == True:
        print("-----Username Selector-----")
        print("The usernames currently in use are ",UsernamesInUse)
        
        Username = input("Enter a non duplicate username, if you enter an already in use username you can change the password. ")
        
        if len(UsernameSaltHashedPassword) > 1:
            for i in range(0, len(UsernameSaltHashedPassword)):
                if Username == UsernameSaltHashedPassword[i][0]:
                    ChangePassword = input("Duplicate Username, Do you want to change the password. Enter Y/N ")
                    if ChangePassword.lower() in ["y","yes","true","t"]:
                        print("Password change has been selected")
                        UsernameSaltHashedPassword.remove(UsernameSaltHashedPassword[i])
                        UsernameDuplicate = False
                        break
                    elif ChangePassword.lower() in ["n","no","false","f"]:
                        print("Password change has been declined, please try another username")
                        continue
                    else:
                        print("Input for Password change not recognised, please try again")
                elif i == len(UsernameSaltHashedPassword)-1:
                    print("Valid Non-Duplicate Username")
                    UsernameDuplicate = False
                    break
        else:
            print("Valid Non-Duplicate Username")
            UsernameDuplicate = False
    
    #Sets variables to ensure while loop will work
    Password = ""
    PasswordCheck = None
    
    while Password != PasswordCheck: #Checks both passwords are the same
        print("-----Password Input-----")
        Password = getpassVsInput("Enter the password for this username, this input will not be echoed in VSC ")
        PasswordCheck = getpassVsInput("Re-enter the same password to confirm ")

    Salt = SaltGenerator() #Creates salt to add to password for hashing
    HashedPassword = Sha512Hash(Password,Salt) #Hashes inputted password with salt
    
    UsernameSaltHashedPassword.append([Username,Salt.hex(),HashedPassword]) #Creates a list of the data to     
    #be written to the csv file, salt.hex is to turn the byte string into a hex string to be appeneded, 
    #the hex string is converted to a byte string
    
    UsernamesInUse.append(Username)
    
    clear() #Clears output for next runthrough

CSVWrite("UsernameSaltHashedPassword",UsernameSaltHashedPassword) #Stores Information to CSV File
