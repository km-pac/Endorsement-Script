import requests, json, time, calendar, difflib
from getpass import getpass
from colorama import Fore, Style

target_url = "https://redmine.leekie.com/issues.json"

params = {
    "project_id": 16,
    "tracker_id": 23
}

user_ids = {
    "Fendi Tan" : 9,
    "Randy Novent" : 151,
    "Stepany Dawn Lacuarta" : 428,
    "Renz Gabriel Dator" : 440,
    "Jhan patric esquivel" : 438,
    "Vincent L. Bandojo" : 446,
    "Faye Angelique Pancho" : 447,
    "Christian Jude G. Ceballos" : 451,
    "Kyle Melvin Pacis" : 456
}


def fetch_latest_endorsement(username, password):
    response = requests.get(target_url, params=params, auth=(username, password))
    previous_end_ids = []
    authors = []
    assigned_tos = []
    subjects = []
    descriptions = []
    endorsement_entries = []
    if response.status_code == 200:
        latest_endorsement = json.loads(response.text)
        for key in latest_endorsement["issues"]:
            previous_end_ids.append(key["id"])
            authors.append(key["author"]["name"])
            assigned_tos.append(key["assigned_to"]["name"])
            subjects.append(key["subject"])
            descriptions.append(key["description"])
            # print(f"ID: {previous_end_ids}\nAssigned by: {authors}\nAssigned to: {assigned_tos}\n{subjects}\n{descriptions}\n\n")
        return previous_end_ids, authors, assigned_tos, subjects, descriptions     
    else:
        print("Error:", response.status_code)
       
         
def close_latest_endorsemnt(previous_end_id, username, password):
    put_url =  f"{target_url.split('.j')[0]}/{previous_end_id}.json"
    # data to be PUT
    data = {
        "issue": {
            "status_id": 5,
            "done_ratio": 100
        }
    }
    response = requests.put(put_url, json=data, params=params, auth=(username, password))
    # Debugging show data placed and response
    # print(data)
    print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS {response.status_code}: {Style.NORMAL}{Fore.RESET}Successfully closed ticket #{previous_end_id}")



def create_new_endorsement(previous_end_id, description, username, password):
    # Time function
    time_struct = time.localtime()
    cur_month = calendar.month_name[time_struct.tm_mon]
    cur_day = time_struct.tm_mday
    cur_year = time_struct.tm_year
    cur_hour = time_struct.tm_hour
    cur_min = time_struct.tm_min
    
    if cur_hour >= 6 and (cur_hour < 14 or cur_min <= 30):
        subject = f"Endorsement Morning to Mid - {cur_month} {cur_day}, {cur_year}"
    elif cur_hour >= 14 and (cur_hour < 22 or cur_min <= 30):
        subject = f"Endorsement Mid to Night - {cur_month} {cur_day}, {cur_year}"
    else:
        subject = f"Endorsement Night to Morning - {cur_month} {cur_day-1}, {cur_year}"
    
    name = input(f"{Fore.GREEN}{Style.BRIGHT}PROMPT{Style.NORMAL}{Fore.RESET}: Endorse this ticket to user => ")
    for user in user_ids: 
        if name.lower() in user.lower(): assigned_to = user
    
    # data to be POSTED
    data = {
      "issue": {
        "project_id": 16,
        "tracker_id": 23,
        "priority_id": 4,
        "assigned_to_id": user_ids[assigned_to],
        "subject": subject,
        "description": f"""
    {description} 
            
Previous Endorsement #{previous_end_id}""",
        "watcher_user_ids": [value for value in user_ids.values()]
      }
    }
    response = requests.post(target_url, json=data, params=params, auth=(username, password))
    # Debugging show data posted and response
    # print(data)
    print(f"\n{Fore.GREEN}{Style.BRIGHT}SUCCESS {response.status_code}: {Style.NORMAL}{Fore.RESET}Successfully created ticket")
    
    
    


