# Blockmole

# Imports

import sqlite3
import time
import os
import requests
import json
from pyfiglet import figlet_format
from prettytable import from_db_cursor, PrettyTable


def clear():
    # Clears the screen entirely
    os.system("cls")
    return

def print_header():
    # Prints the nice Blockmole menu header :)
    print(figlet_format("Blockmole"))
    return

def get_address_info(address):
    # Requests a certain Bitcoinaddress via blockchain-API and returns a list
    response = requests.get("https://blockchain.info/balance?active=" + address)
    response_list = json.loads(response.text)
    return response_list

def pretty_table(cursor, casenumber):
    # Takes the cursor and tablenumbers and puts the SQLite data into a nice pretty table
    cursor.execute("SELECT * FROM %s" % casenumber)
    prettytable = from_db_cursor(cursor)
    return prettytable

def user_show_existing():
    files = filter(os.path.isfile, os.listdir(os.curdir))
    files_db = [fi for fi in files if fi.endswith(".db")]
    clear()
    print("\n### Existing casefiles ###\n")
    for i in files_db:
        print(" - " + str(i))
    return

def user_create(username):
    connect = sqlite3.connect(str(username)+'.db')
    cursor = connect.cursor()
    db_loaded = True
    print("\n### Database loaded! ###\n")
    time.sleep(1)
    return db_loaded


def print_state(db_loaded, case_loaded, db_name, case_name):
    if db_loaded == True:
            print("     # User %s logged in!" % str(db_name))
    else:
        print("     # No user active. Please load a userfile!")
    if case_loaded == True:
        print("     # Case %s loaded and active!\n"  % str(case_name))
    else:
        print("     # No case loaded. Please load a case!\n")
    return


def print_menu(db_loaded, case_loaded):
    if db_loaded == False:
        print("[1] - Show existing userfiles")
        print("[2] - Create or load a userfile\n")
        print("[0] - Exit Blockmole\n")
           

    elif db_loaded == True and case_loaded == False:
        print("[1] - Show existing casefiles")
        print("[2] - Create or edit a casefile\n")
        print("[0] - Exit Blockmole\n")
        

    elif db_loaded == True and case_loaded == True:
        print("[1] - Show bitcoinaddresses in this case")
        print("[2] - Add bitcoinaddress to this case")
        print("[3] - Update transactiondata")
        print("[4] - Show addresses with new TXs\n")
        print("[0] - Exit Blockmole\n")
    return


def main():

    program_active = True
    db_loaded = True
    case_loaded = True
    db_name = "Matthias"
    case_name = "123456_2018"
    clear()

    while program_active == True:
        clear()
        print_header()
        print("\n")
        print("Welcome to Blockmole - a simple Bitcoinaddress Trackingtool\n")
        print("    > Current status:")
        print_state(db_loaded, case_loaded, db_name, case_name)
        print_menu(db_loaded, case_loaded)
        
        user_prompt = input("blockmole >> ")   

    
    
if __name__ == '__main__':
    main()

