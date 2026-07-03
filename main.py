#THIS IS THE MAIN ENTRY POINT FOR THIS PROJECT
#THIS IS WHERE ALL OPERATIONS WILL BE HANDLED

import modules.storage as storage,modules.analytics as analytics,modules.Loger as Loger
from datetime import date
import argparse as agp

#HANDLES THE CLI WORK
parser = agp.ArgumentParser (description = "--- Study Session Tracker ---")
parser.add_argument( "command" ,choices = ["add","stats", "config","goal"] ,help = "Action to be taken" )
arg = parser.parse_args()
command = arg.command

#HANDLES THE INPUT TAKEN FROM CLI

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
        for c,s in analytics.stat_choices.items():
            print(f"{c}.{s}",end = "\n")
        ch = (input("Choice for stat : "))
        analytics.manage_analytics(ch)
    
    elif (command == "goal"):
        pass
    
    elif (command == "config"):
        pass
    
    
Handler(command)