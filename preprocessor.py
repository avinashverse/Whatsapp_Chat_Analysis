import pandas as pd
import re
from datetime import datetime
def preprocess(data):
    # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # messages = re.split(pattern , data)[1:]
    # dates = re.findall(pattern , data) 
    # df = pd.DataFrame({'user_message' : messages , 'date':dates}) 
    # df['date'] = df['date'].str.split(' - ')
    # df['date'] = df['date'].apply(lambda x: x[0])
    # df['date'] = pd.to_datetime(df['date'])
    

    date_formats = [
        "%m/%d/%y, %H:%M",
        "%m/%d/%y, %I:%M %p",
        "%m/%d/%Y, %H:%M",
        "%m/%d/%Y, %I:%M %p",
        "%d/%m/%Y, %H:%M",
        "%d/%m/%Y, %I:%M %p",
        "%d/%m/%y, %H:%M",
        "%d/%m/%y, %I:%M %p",
        "%Y/%m/%d, %H:%M",
        "%Y/%m/%d, %I:%M %p",
        "%y/%m/%d, %H:%M",
        "%y/%m/%d, %I:%M %p"
    ]

    parsed_dates = []
    messages = []

    for line in data.split('\n'):
        if line:
            parts = line.split(" - ")
            if len(parts) == 2:
                timestamp, message = parts
                for date_format in date_formats:
                    try:
                        parsed_date = datetime.strptime(timestamp.strip(), date_format)
                        parsed_dates.append(parsed_date)
                        messages.append(message.strip())
                        break
                    except ValueError:
                        continue

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'date': parsed_dates})

    

    users = [] 

    messages = [] 
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s' , message) 
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]) ) 
        else:
            users.append("group_notification") 
            messages.append(entry[0]) 
    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['user_message']  , inplace = True) 
    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df['message'] = df['message'].replace("<Media omitted>" , "Media_file")
    return df 