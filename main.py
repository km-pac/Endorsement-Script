from skypepull import *
from redminepush import *
import os
from colorama import Fore, Style


os.system('cls')

# Fetch Endorsement ticket from skype
token_loc = "token"
endorsement_thread_id = "19:f47c3501aa2c402f8fefbd8643489311@thread.skype"
sk = connect_skype("lkejna1022@gmail.com","vortvbgkfpqlhuiv",token_loc)
description = fetch_description(endorsement_thread_id, sk)

# Push the ticket to Redmine
print(f"{Fore.YELLOW}{Style.BRIGHT}\n\t\t ===== Redmine Ticket Endorsement ===== \t\t\n{Style.NORMAL}{Fore.RESET}")

username = input(f"{Fore.GREEN}{Style.BRIGHT}PROMPT{Style.NORMAL}{Fore.RESET}: Enter your username => ")
password = getpass(f"{Fore.GREEN}{Style.BRIGHT}PROMPT{Style.NORMAL}{Fore.RESET}: Enter your password => ")

try:
    previous_end_ids, authors, assigned_tos, subjects, descriptions = fetch_latest_endorsement(username, password)
except: print(f"\n{Fore.RED}{Style.BRIGHT}ERROR{Style.NORMAL}{Fore.RESET}: Authentication failed")

try:
    if previous_end_ids != None:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\n\nSigned in as: {username}\n{Style.NORMAL}{Fore.RESET}")    
        
        # Previously Assigned Ticket
        print(f"{Fore.BLUE}{Style.BRIGHT}\t\t ----- PREVIOUSLY ASSIGNED ENDORSEMENT ----- \t\t\n")
        for index, previous_end_id in enumerate(previous_end_ids):
            print(f"#{previous_end_id}")
            print(f"Author: {authors[index]}")
            print(f"Assigned to: {assigned_tos[index]}\n")
            print(f"{subjects[index]}\n")
            print(f"{descriptions[index]}\n{Style.NORMAL}{Fore.RESET}")

        # Ticket to be endoresed
        print(f"{Fore.CYAN}{Style.BRIGHT}\n\t\t ----- ENDORSEMENT TICKET CREATED ----- \t\t\n")
        print(f"{description}\n\n{Style.NORMAL}{Fore.RESET}")
        
        # Create new ticket and endorse to user
        create_new_endorsement(previous_end_ids[0], description, username, password)
        
        # Close previous ticket
        close_latest_endorsemnt(previous_end_ids[0], username, password)
    
except: print(f"\n{Fore.RED}{Style.BRIGHT}ERROR{Style.NORMAL}{Fore.RESET}: Failed to push endorsement ticket to Redmine")
