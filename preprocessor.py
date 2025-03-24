import re
import pandas as pd

def preprocess(data):
    pattern = r"\[(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} ?[APM]{2})\] ([^:]+): (.*)"
    
    matches = re.findall(pattern, data)
    messages = []
    time_info = []
    senders = []
    for match in matches:
        timestamp, sender, message = match
        messages.append(message)
        time_info.append(timestamp)
        senders.append(sender)

    def extract_datetime_components(timestamps):
        dates = []      
        months = []   
        years = []      
        hour_list = []  
        min_list = []  
        sec_list = [] 
        
        for timestamp in timestamps:
            date_part, time_part = timestamp.split(", ")
            
            day, month, year = map(int, date_part.split("/"))
            year = 2000 + year 
            
            time_str = time_part.split("\u202f")[0]  
            period = time_part.split("\u202f")[1]  
            hr, min, sec = map(int, time_str.split(":")) 
            
            if period == "PM" and hr != 12:
                hr += 12
            elif period == "AM" and hr == 12:
                hr = 0
                
            dates.append(day)
            months.append(month)
            years.append(year)
            hour_list.append(hr)
            min_list.append(min)
            sec_list.append(sec)
        
        return dates, months, years, hour_list, min_list, sec_list

    dates, months, years, hours, minutes, seconds = extract_datetime_components(time_info)
    df = pd.DataFrame({'sender':senders, 'user_message': messages})
    df['date'] = dates
    df['month'] = months
    df['year'] = years
    df['hours'] = hours
    df['minutes'] = minutes
    df['seconds'] = seconds
    def convert_month_to_name(month_num):
        month_dict = {
            1: 'January',
            2: 'February', 
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        return month_dict[month_num]

    months_list = df['month'].tolist()
    month_names = [convert_month_to_name(month) for month in months_list]

    df['month'] = month_names

    df['sender'] = df['sender'].replace({
    'Sumacom Consultancy Pvt. Ltd': 'Group Notifications'
    })

    return df


