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
    clear()
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

def menu_structure(menu_number, db_loaded, db_name, case_loaded, case_name):
    clear()
    print_header()
    print("\n")
    print("Welcome to Blockmole - a simple Bitcoinaddress Trackingtool\n")
    print("    > Current status:")
    if db_loaded == True:
        print("     # User %s logged in!"%str(db_name))
    else:
        print("     # No user active. Please load a userfile!")
    if case_loaded == True:
        print("     # Case %s loaded and active!\n"  % str (case_name))
    else:
        print("     # No case loaded. Please load a case!\n")

    if menu_number == 0:
        print("test")
    
    return



def main():
    program_active = True
    while program_active == True:
                
        menu_structure(0, True, "Matthias", False, "123456/2018")
        user_prompt = input("blockmole >>")
        if user_prompt == "2":
            program_active = False

    return






if __name__ == '__main__':
    main()

