# Blockmole

# Imports

import sqlite3
import time
import os
import requests
import json
from pyfiglet import figlet_format
from prettytable import from_db_cursor, PrettyTable


# Functions

def clear():
    # Clears the screen entirely
    os.system("cls")
    return


def get_address_info(address):
    # Requests a certain Bitcoinaddress via blockchain-API and returns a list
    response = requests.get("https://blockchain.info/balance?active=" + address)
    response_list = json.loads(response.text)
    return response_list


def user_show_existing():
    # Scans the installationfolder for *db files and lists them
    freeze = True
    while freeze == True:
        files = filter(os.path.isfile, os.listdir(os.curdir))
        files_db = [fi for fi in files if fi.endswith(".db")]
        clear()
        print("\n### Existing userfiles ###\n")
        for i in files_db:
            print(" - " + str(i) + "")
        print("\n[1] - Back to menu\n")
        var_menu = user_prompt()
        if var_menu == "1":
            freeze = False
        else:
            print("Invalid entry! Please try again")
            time.sleep(1)
        
    return

def user_prompt():
    # Simple userprompt
    prompt = input("blockmole >> ")
    return prompt


def user_create(username):
    # Creates a new SQLite DB
    connect = sqlite3.connect(str(username)+'.db')
    connect.close()
    db_loaded = True
    print("\n### Logged in! ###\n")
    time.sleep(2)
    
    return db_loaded

def case_create(db_name, case_name):
    # Creates a table (a case) in the given SQLite Database
    connect = sqlite3.connect(str(db_name)+'.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS [%s] (
                    address_number INTEGER PRIMARY KEY,
                    address TEXT,
                    date_added TEXT,
                    has_transaction BOOLEAN,
                    last_used FLOAT,
                    comment TEXT);""" % case_name)
    connect.commit()
    connect.close()
    print("Case successfully created!")
    time.sleep(1)
    return True


def print_header():
    # Prints the nice Blockmole menu header :)
    print(figlet_format("Blockmole"))
    return


def print_state(db_loaded, case_loaded, db_name, case_name):
    # Prints the small status screen in the menu
    if db_loaded == True:
            print("#  User:      %s" % str(db_name))
    else:
        print("#  No user active. Please load a userfile!")
    if case_loaded == True:
        print("#  Case:      %s\n"  % str(case_name))
    else:
        print("#  No case loaded. Please load a case!\n")
    return


def print_menu(db_loaded, case_loaded):
    # Prints the menu
    if db_loaded == False:
        print("[1] - Show existing userfiles")
        print("[2] - Create or load a userfile\n")
        print("[0] - Exit Blockmole\n")
           

    elif db_loaded == True and case_loaded == False:
        print("[1] - Show existing casefiles")
        print("[2] - Create or load a casefile\n")
        print("[0] - Exit Blockmole\n")
        

    elif db_loaded == True and case_loaded == True:
        print("[1] - Show bitcoinaddresses in this case")
        print("[2] - Add bitcoinaddress to this case")
        print("[3] - Update transactiondata")
        print("[4] - Show addresses with new TXs\n")
        print("[0] - Exit Blockmole\n")

    return


def pretty_table(cursor, casenumber):
    # Takes the cursor and tablenumbers and puts the SQLite data into a nice pretty table
    cursor.execute("SELECT * FROM %s" % casenumber)
    prettytable = from_db_cursor(cursor)
    return prettytable


def main():
    # Main
    program_active = True
    db_loaded = False
    case_loaded = False
    db_name = ""
    case_name = ""
    clear()

    while program_active == True:
        clear()
        print_header()
        print("Welcome to Blockmole - a simple Bitcoinaddress Trackingtool\n")
        print("> Current status:\n")
        print_state(db_loaded, case_loaded, db_name, case_name)
        print("\n")
        print_menu(db_loaded, case_loaded)
        
        var_menu = user_prompt()

        # User menu
        if var_menu == "1" and db_loaded == False:
            print("\nExisting userfiles:")
            user_show_existing()  
        elif var_menu == "2" and db_loaded == False:
            print("\nPlease enter a username: \n")
            db_name = user_prompt()
            db_loaded = user_create(db_name)

        # Case menu
        elif var_menu == "1" and db_loaded == True:
            pass
        elif var_menu == "2" and db_loaded == True:
            print("\nPlease enter the casenumber: \n")
            case_name = user_prompt()
            case_loaded = case_create(db_name, case_name)

        # Tracking menu
        elif var_menu == "1" and db_loaded == True and case_loaded == True:
            pass
        elif var_menu == "2" and db_loaded == True and case_loaded == True:
            pass
        elif var_menu == "3" and db_loaded == True and case_loaded == True:
            pass

        elif var_menu == "0":
            program_active = False
        
        else:
            print("# Invalid entry. Please retry! #")
            time.sleep(1)
    
    
if __name__ == '__main__':
    main()

