import os, time, sys, re
from skpy import Skype
from skpy import SkypeAuthException
from datetime import datetime, timedelta
from colorama import Fore, Style


def connect_skype(user, pwd, token):  
    s = Skype()  
    s.conn.setTokenFile(token)  
    try:  
        s.conn.readToken()  
    except SkypeAuthException:  
        s.conn.setUserPwd(user, pwd)  
        s.conn.getSkypeToken()  
        s.conn.writeToken()  
    finally:  
        sk = Skype(user, pwd, tokenFile=token)  
    return sk

def fetch_description(endorsement_thread_id, sk):
    ch = sk.chats[endorsement_thread_id]
    messages = ch.getMsgs()

    for index, message in enumerate(messages):
        description = message.content
        if "Things" in description: parsed_desc = description.split("<e_m")[0]
    return parsed_desc






