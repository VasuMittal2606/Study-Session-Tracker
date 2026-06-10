import storage,analytics,Loger
from datetime import date
import argparse as agp
parser = agp.ArgumentParser (description = "--- Study Session Tracker ---")
parser.add_argument( "command" ,choices = ["add","stats", "config","goal"] ,help = "Action to be taken" )
arg = parser.parse_args()
command = arg.command

def inp():
    data = {}
    data["subject"] = input("Subject : ")
    data["topic"]= input("Topic : ")
    data["date"] = date.today().isoformat()
    while True:
        try:
            data["duration"] = float(input("Duration(in hrs) : "))
            break
        except ValueError:
            print("Wrong Time, try again")
    return data

def Handler( command ):


    if (command == "add"):
        storage.csv_storing(inp())


    elif (command == "stats"):
        pass
    
    elif (command == "goal"):
        pass
    
    elif (command == "config"):
        pass
    
    


Handler(command)