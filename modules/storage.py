#THIS FILE HANDLES THE CSV STORING OF STUDY SESSIONS
#THIS WILL ALSO BE USED BY ANALYTICS FOR PRESENTING DIFFERENT STATS

import csv
from pathlib import Path
filename = "sessions.csv"
fields = ["subject","topic","duration","date"]


def csv_storing(data_dict):
    file = Path(filename)

    #checks if file exists or not
    #also if the file is empty or not

    header_needed = ( (not file.exists()) or (file.stat().st_size == 0) )    
    
    with open(filename, "a" , newline = "") as csv_file:
        writer = csv.DictWriter(csv_file , fieldnames = fields)

        #if the created file is empty, it adds its header
        
        if header_needed :
            writer.writeheader()
        
        writer.writerow(data_dict)
    print("Session Saved Successfully")
    return data_dict

# FUTURE SCOPE FOR DELETION AND UPDATION
# def delete_data():
#     pass