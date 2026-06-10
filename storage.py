import csv
from pathlib import Path
filename = "sessions.csv"
fields = ["subject","topic","duration","date"]


def csv_storing(data_dict):
    file = Path(filename)
    header_needed = ( (not file.exists()) or (file.stat().st_size == 0) )    
    
    with open(filename, "a" , newline = "") as csv_file:
        writer = csv.DictWriter(csv_file , fieldnames = fields)
        if header_needed :
            writer.writeheader()
        
        writer.writerow(data_dict)
    print("Session Saved Successfully")
    return data_dict


