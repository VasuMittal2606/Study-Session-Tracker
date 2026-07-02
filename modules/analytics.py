# WEEKLY REPORTS CONTAINING 
# MOST STUDIED SUBJECT
# TOTAL STUDY HOURS/SESSIONS  ||  HOURS PER SUBJECT  ||  MOST STUDIED SUBJECT  || 
# SESSIONS PER DAY  ||  DAILY STUDY HOURS  ||  
# WEEKLY SUMMARY  ||  GOAL PROGRESS  ||

import csv
import modules.storage as storage
# import storage

file = storage.filename



def get_stats():
    with open(file,'r',newline='') as csv_data:
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
            "sub-wise_hours" : sub_hours,
            # "daily_hours" : daily_hours
            }

max_sub = 0


def most_studied_sub():
    # with open(file,'r',newline='') as csv_data:
    #     data = csv.DictReader(csv_data)
    # for i in data:
    #     print(i)
    pass