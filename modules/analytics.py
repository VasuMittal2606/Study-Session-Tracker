# WEEKLY REPORTS CONTAINING 
# MOST STUDIED SUBJECT
# TOTAL STUDY HOURS/SESSIONS  ||  HOURS PER SUBJECT  ||  MOST STUDIED SUBJECT  || 
# SESSIONS PER DAY  ||  DAILY STUDY HOURS  ||  
# WEEKLY SUMMARY  ||  GOAL PROGRESS  ||

import csv
from pathlib import Path
if __name__ == "__main__" :
    import storage
else:
    import modules.storage as storage

filename = storage.filename
file_path = Path(filename)


def check():
    if (not file_path.exists() ) or (file_path.stat().st_size == 0):
        print("No study sessions found yet")
        exit()
        

def get_stats():
    with open(filename,'r',newline='') as csv_data:
        data = csv.DictReader(csv_data)
        total_sessions = 0
        total_hours = 0
        sub_hours = {}
        # daily_hours = {}
        for i in data:
            total_sessions += 1
            duration = float(i['duration'])
            total_hours += duration
            # print(i)
            if i["subject"] not in sub_hours:
                sub_hours[i["subject"]] = duration
            else:
                sub_hours[i["subject"]] += duration
            
    return {"total_sessions" : total_sessions ,
            "total_hours" : total_hours, 
            "subject_hours" : sub_hours,
            # "daily_hours" : daily_hours
            }



def most_studied_sub(stats):
    
    max_sub = {"Subjects":[] , "Hours": 0 }
    sub_wise_stats = stats["subject_hours"]
    max_hours = max( sub_wise_stats.values() )
    for sub,hrs in sub_wise_stats.items():
        if(hrs == max_hours):
            max_sub["Subjects"].append(sub)
            max_sub["Hours"]=max_hours
    return max_sub

# print(most_studied_sub(stats))
stat_choices = {
            "1":"Basic Stats" , 
            "2":"Most Studied subject" , 
            "3":"Hours per subject" , 
            "4":"None"
           }

def manage_analytics(choice):
    #THIS FUNCTION MANAGES THE ANALYTICS PRINTED
    check()
    stats = get_stats()
    sub_wise_stats = stats["subject_hours"]
    total_sesh = stats["total_sessions"]
    total_hrs = stats["total_hours"]

    if (choice == "1"):
        print("Total Study hours : ",total_hrs)
        print("Total Study sessions : ",total_sesh)

    elif (choice == "2"):
        print(most_studied_sub(stats))

    elif (choice == "3"):
        print(sub_wise_stats)

    elif (choice == "4"):
        print("Coming soon")

    else:
        pass
        print("Wrong choice, Try again")



if __name__ == "__main__":
    manage_analytics()