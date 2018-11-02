# Blockmole

#######################################################
# Imports
#######################################################

import sqlite3
import time
import os
import requests
import json
from pyfiglet import figlet_format
from prettytable import from_db_cursor, PrettyTable
from blockchain import blockexplorer

#######################################################
# Classes
#######################################################

class BitcoinAddress:
    """
    This is a class for Bitcoinaddresses with all relevant data stored
    """
    def __init__(self, address, n_tx, total_received, total_sent, balance, last_tx_date, data_created_date):
        
        self.address = address
        self.n_tx = n_tx
        self. total_received = total_received
        self.total_sent = total_sent
        self.balance = balance
        self.last_tx_date = last_tx_date
        self.data_created_date = 0
    
    def build(address):
        api_address = blockexplorer.get_address(address)
        api_transactions = api_address.transactions
        n_tx = api_address.n_tx
        total_received = api_address.total_received
        total_sent = api_address.total_sent
        balance = api_address.final_balance
        last_tx_date = api_transactions[-1].time
        data_created_date = 0
        final_object = BitcoinAddress(address, n_tx, total_received, total_sent, balance, last_tx_date, data_created_date)
        return final_object

#######################################################
# Functions
#######################################################

#######################################################
## Standards:
#######################################################

def clear():
    # Clears the screen entirely
    os.system("cls")
    return

def user_prompt():
    prompt = input("blockmole >> ")
    return prompt

#######################################################
## Databasefunctions:
#######################################################

def database_list_existing():
    # Scans the installationfolder for *db files and returns them as list
    files = filter(os.path.isfile, os.listdir(os.curdir))
    files_db = [fi for fi in files if fi.endswith(".db")]
    return files_db

def database_check_existing(dbname):
    # Checks if the database already exists and returns True or False
    files = database_list_existing()
    if any(str(dbname) in s for s in files):
        return True
    else:
        return False

def database_create_new(dbname):
    # Creates a new SQLite DB File
    connect = sqlite3.connect(str(dbname))
    connect.close()
    return True

def database_delete_existing(dbname):
    # Deletes a given SQLite Databasefile
    os.remove(str(dbname))
    return
    

#######################################################
## Tablefunctions
#######################################################

def case_create(db_name, case_name):
    # Creates a table in the given SQLite DB
    connect = sqlite3.connect(str(db_name))
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS [%s] (
                    address_number INTEGER PRIMARY KEY,
                    address TEXT,
                    n_tx FLOAT,
                    total_received FLOAT,
                    total_sent FLOAT,
                    last_tx TEXT,
                    date_added TEXT,
                    balance FLOAT,
                    comment TEXT);""" % case_name)
    connect.commit()
    connect.close()
    print("Case %s successfully created!" % case_name)
    time.sleep(1)
    return True

def case_delete(db_name, case_name):
    connect = sqlite3.connect(str(db_name))
    cursor = connect.cursor()
    try:
        cursor.execute("""DROP TABLE [%s]""" % case_name)
        connect.commit()
        connect.close()
        print("Case %s successfully deleted!" % case_name)
        time.sleep(1)
    except:
        print("Case %s not existing!" % case_name)
        time.sleep(1)
    return False


#######################################################
## Printfunctions
#######################################################

def print_header():
    # Prints the Blockmole menu header
    print(figlet_format("Blockmole V0.2"))
    return

def print_state(db_loaded, case_loaded, db_name, case_name):
    # Prints a small status screen in the menu
    if db_loaded == True:
        print("#  User:      %s" % str(db_name))
    else:
        print("#  No user active. Please load a userfile!")
    if case_loaded == True:
        print("#  Case:      %s\n"  % str(case_name))
    else:
        print("#  No case loaded. Please load a case!\n")
    return

def print_main_menu(db_loaded, case_loaded):
    # Prints the menu
    if db_loaded == False:
        print("[1] - Show existing userfiles")
        print("[2] - Create a userfile")
        print("[3] - Delete a userfile\n")
        print("[0] - Exit Blockmole\n")
           
    elif db_loaded == True and case_loaded == False:
        print("[1] - Show existing casefiles")
        print("[2] - Create or load a casefile")
        print("[3] - Delete a casefile\n")
        print("[4] - Unload the userfile\n")
        print("[0] - Exit Blockmole\n")
        
    elif db_loaded == True and case_loaded == True:
        print("[1] - Show bitcoinaddresses in this case")
        print("[2] - Add bitcoinaddress to this case")
        print("[3] - Update transactiondata")
        print("[4] - Show addresses with new TXs\n")
        print("[5] - Unload the casefile\n")
        print("[0] - Exit Blockmole\n")

    return

def print_load_database():
    freeze = True
    while freeze == True:
        clear()
        files = database_list_existing()
        print_header()
        print("\n### Existing userfiles ###\n")
        count = 1
        for i in files:
            print("["+str(count)+"] - " + str(i))
            count += 1
        print("\n")
        print("[0] - Back to menu\n")
        load_menu = user_prompt()
        if load_menu == "0":
            return {"db_loaded": False, "db_name": ""}
        else:
            try: 
                db_name = str(files[int(load_menu)-1])
                database_create_new(db_name)
                print("### Database loaded ###")
                time.sleep(1)
                return {"db_loaded": True, "db_name": str(db_name)}
            except:
                print("### File not existing ###")
                time.sleep(1)
                return {"db_loaded": False, "db_name": ""}

def print_create_database():
    clear()
    print_header()
    print("\nPlease enter a username: \n")
    db_name = user_prompt()+".db"
    if database_check_existing(db_name) == True:
        print("Userfile already existing. Loading file...\n")
        database_create_new(db_name)
        time.sleep(1)
        print("### Userfile loaded! ###")
        return {"db_loaded": True, "db_name": str(db_name)}
        
    else:
        print("Userfile not existing. Creating file...\n")
        db_loaded = database_create_new(db_name)
        time.sleep(1)
        print("### Userfile created and loaded! ###")
        return {"db_loaded": True, "db_name": str(db_name)}

def print_delete_database():
    freeze = True
    while freeze == True:
        clear()
        files = database_list_existing()
        print_header()
        print("\n### Existing userfiles ###\n")
        count = 1
        for i in files:
            print("["+str(count)+"] - " + str(i))
            count += 1
        print("\n")
        print("[0] - Back to menu\n")
        delete_menu = user_prompt()
        if delete_menu == "0":
            return {"db_loaded": False, "db_name": ""}
        else:
            try: 
                db_name = str(files[int(load_menu)-1])
                database_delete_existing(db_name)
                print("### Database successfully deleted! ###")
                time.sleep(1)
                return {"db_loaded": False, "db_name": ""}
            except:
                print("### File not existing, please retry! ###")
                time.sleep(1)
                return {"db_loaded": False, "db_name": ""}

def pretty_table(firstrow, contents):
    t = PrettyTable(firstrow)
    for row in contents:
        t.add_row(row)
    return t


#######################################################
## Main
#######################################################

def main():
    program_active = True
    db_loaded = False
    case_loaded = False
    db_name = ""
    case_name = ""

    while program_active == True:
        clear()
        print_header()
        print("Welcome to Blockmole - a simple Bitcoinaddress Trackingtool\n")
        print("> Current status:\n")
        print_state(db_loaded, case_loaded, db_name, case_name)
        print("\n")
        print_main_menu(db_loaded, case_loaded)
        
        var_menu = user_prompt()

        # Database menu
        if db_loaded == False and case_loaded == False:
            if var_menu == "1":
                result = print_load_database()
                db_loaded = result["db_loaded"]
                db_name = result["db_name"]
            elif var_menu == "2":
                result = print_create_database()
                db_loaded = result["db_loaded"]
                db_name = result["db_name"]
            elif var_menu == "3":
                result = print_delete_database()
                db_loaded = result["db_loaded"]
                db_name = result["db_name"] 

        elif db_loaded == True and case_loaded == False:


        elif var_menu == "0":
            program_active = False
        

#######################################################
## Launcher
#######################################################

if __name__ == '__main__':
    main()