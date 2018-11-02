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
    def __init__(self, address, n_tx, total_received, total_sent, balance, last_tx_date, data_created_date, comment):
        
        self.address = address
        self.n_tx = n_tx
        self.total_received = total_received
        self.total_sent = total_sent
        self.balance = balance
        self.last_tx_date = last_tx_date
        self.data_created_date = 0
        self.comment = comment
    
    def build(address, comment):
        # Builds the object with given attributes
        api_address = blockexplorer.get_address(address)
        api_transactions = api_address.transactions
        n_tx = api_address.n_tx
        total_received = api_address.total_received
        total_sent = api_address.total_sent
        balance = api_address.final_balance
        last_tx_date = api_transactions[-1].time
        data_created_date = 0
        final_object = BitcoinAddress(address, n_tx, total_received, total_sent, balance, last_tx_date, data_created_date, comment)
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
    # Standard user input
    prompt = input("blockmole >> ")
    return prompt

def sql_string_cleanup(string):
    # Takes a given SQL string and returns it clean
    string2 = str(string)
    string3 = string2.replace("(\'", "")
    string4 = string3.replace("\',)", "")
    return string4

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
    try:  
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
        return True
    except:
        return False
    return {"case_loaded": True, "case_name": case_name}


def case_delete(db_name, case_name):
    # Deletes a table in given database
    connect = sqlite3.connect(str(db_name))
    cursor = connect.cursor()
    cursor.execute("""DROP TABLE [%s]""" % case_name)
    connect.commit()
    connect.close()
    print("Case %s successfully deleted!" % case_name)
    time.sleep(1)
      

def case_show_existing(dbname):
    # Parses the given SQL File for tables and returns a clean list of tablenames
    connect = sqlite3.connect(dbname)
    cursor = connect.cursor()
    tables = cursor.execute("SELECT tbl_name FROM sqlite_master")
    contents = []
    for row in tables.fetchall():
        string = sql_string_cleanup(row)
        contents.append(string)
    connect.close()
    return contents

def case_write_into_db(db_name, case_name, address_list):
    pass

def case_load_into_object(dbname, case_name):
    # Loads SQLite data into a list of python objects
    connect = sqlite3.connect(dbname)
    cursor = connect.cursor()
    i = 0
    address_list = []
    try:
        for row in cursor.execute("SELECT * FROM [%s]" % case_name):
            address = sql_string_cleanup(cursor.execute("SELECT address FROM [%s] WHERE rowid = %s" % case_name, i))
            n_tx = sql_string_cleanup(cursor.execute("SELECT n_tx FROM [%s] WHERE rowid = %s" % case_name, i))
            total_received = sql_string_cleanup(cursor.execute("SELECT total_received FROM [%s] WHERE rowid = %s" % case_name, i))
            total_sent = sql_string_cleanup(cursor.execute("SELECT total_sent FROM [%s] WHERE rowid = %s" % case_name, i))
            last_tx = sql_string_cleanup(cursor.execute("SELECT last_tx FROM [%s] WHERE rowid = %s" % case_name, i))
            balance = sql_string_cleanup(cursor.execute("SELECT balance FROM [%s] WHERE rowid = %s" % case_name, i))
            date_added = sql_string_cleanup(cursor.execute("SELECT date_added FROM [%s] WHERE rowid = %s" % case_name, i))
            comment = sql_string_cleanup(cursor.execute("SELECT comment FROM [%s] WHERE rowid = %s" % case_name, i))
            
            i += 1

            final_object = BitcoinAddress(address, n_tx, total_received, total_sent, balance, last_tx, date_added, comment)
            address_list.append(final_object)
    except:
        print("Error loading the database into objects")

    connect.close()
    return address_list


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
    # Launches a menu to load an existing database
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
    # Launches a menu to create and load a new database
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
    # Launches a menu to delete a database
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
                db_name = str(files[int(delete_menu)-1])
                database_delete_existing(db_name)
                print("### Database successfully deleted! ###")
                time.sleep(1)
                return {"db_loaded": False, "db_name": ""}
            except:
                print("### File not existing, please retry! ###")
                time.sleep(1)
                return {"db_loaded": False, "db_name": ""}

def pretty_table(firstrow, contents):
    # Takes two lists and returns a pretty table
    t = PrettyTable(firstrow)
    for row in contents:
        t.add_row(row)
    return t

def print_load_tables(dbname):
    # Prints all existing tables from given SQLite DB and lets the user choose one
    freeze = True
    while freeze == True:
        clear()
        contents = case_show_existing(dbname)
        print_header()
        print("\n### Existing casefiles in this database ###\n")
        count = 1
        for i in contents:
            print("["+str(count)+"] - " + str(i))
            count += 1
        print("\n")
        print("[0] - Back to menu\n")
        case_menu = user_prompt()
        if case_menu == "0":
            return {"case_loaded": False, "case_name": ""}
        else:
            try: 
                case_name = str(contents[int(case_menu)-1])
                address_list = case_load_into_object(dbname, case_name)
                print("### Database loaded ###")
                time.sleep(1)
                return {"case_loaded": True, "case_name": str(case_name), "address_list": address_list}
            except:
                print("### Case not existing ###")
                time.sleep(1)
                return {"case_loaded": False, "case_name": ""}

def print_create_table(dbname):
    freeze = True
    while freeze == True:
        clear()
        print_header()
        print("\n Please enter a casenumber: \n")
        case_name = user_prompt()
        try:  
            connect = sqlite3.connect(str(dbname))
            cursor = connect.cursor()
            cursor.execute("""CREATE TABLE [%s] (
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
            print("Case successfully created!")
            time.sleep(1)
            return {"case_loaded": True, "case_name": case_name}
        except:
            print("Case is already existing! Please load your case!")
            time.sleep(1)
            return {"case_loaded": False, "case_name": ""}

def print_delete_tables(dbname):
    # Prints all existing tables from given SQLite DB and lets the user choose one
    freeze = True
    while freeze == True:
        clear()
        contents = case_show_existing(dbname)
        print_header()
        print("\n### Existing casefiles in this database ###")
        print("Please choose which file to delete: \n")
        count = 1
        for i in contents:
            print("["+str(count)+"] - " + str(i))
            count += 1
        print("\n")
        print("[0] - Back to menu\n")
        case_menu = user_prompt()
        if case_menu == "0":
            return
        else:
            try: 
                case_name = str(contents[int(case_menu)-1])
                case_delete(dbname, case_name)
                time.sleep(1)
                return 
            except:
                print("### Case not existing ###")
                time.sleep(1)
                return

def print_add_address():
    # Takes an address and a comment and returns a bitcoinaddressobject
    clear()
    print_header()
    print("Please enter a bitcoinaddress: \n")
    address_input = user_prompt()
    address_comment = ""
    print("Feel free to enter a comment to this address: \n")
    address_comment = user_prompt()
    final_object = BitcoinAddress.build(address_input, address_comment)
    return final_object

def print_address_existing(address_list):
    # Takes the addresslist and prints a nice table with the items in it
    freeze = True
    clear()
    print_header()
    while freeze == True:
        t = PrettyTable(["Address", "No. of TX", "t.received", "t.sent", "Balance", "Last TX", "Comment"])
        for i in address_list:
            t.add_row([str(i.address), str(i.n_tx), str(i.total_received), str(i.total_sent), str(i.balance), str(i.last_tx_date), str(i.comment)])
        print("\n")
        print(t)
        print("[0] - Back to main menu")
        if user_prompt() == "0":
            freeze = False
        else:
            print("Invalid entry, retry!")
    
#######################################################
## Main
#######################################################

def main():
    program_active = True
    db_loaded = False
    case_loaded = False
    db_name = ""
    case_name = ""
    # a list of Bitcoinaddressobjects:
    address_list = []

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

            elif var_menu == "0":
                program_active = False
            else:
                print("Invalid entry, retry!")
                time.sleep(1)

        # Case menu
        elif db_loaded == True and case_loaded == False:
            if var_menu == "1":
                result = print_load_tables(db_name)
                case_loaded = result["case_loaded"]
                case_name = result["case_name"]
                address_list = result["address_list"]
            elif var_menu == "2":
                result = print_create_table(db_name)
                case_loaded = result["case_loaded"]
                case_name = result["case_name"]
            elif var_menu == "3":
                print_delete_tables(db_name)
            elif var_menu == "4":
                db_loaded = False
                db_name = ""
                print("Userfile not loaded any more. Please select a userfile...")
                time.sleep(2)
            
            elif var_menu == "0":
                program_active = False
            else:
                print("Invalid entry, retry!")
                time.sleep(1)

        # Main menu Tracking
        elif db_loaded == True and case_loaded == True:
            if var_menu == "1":
                print_address_existing(address_list)
            elif var_menu == "2":
                new_object = print_add_address()
                address_list.append(new_object)
            elif var_menu == "3":
                pass
            elif var_menu == "4":
                pass
            elif var_menu == "5":
                case_loaded = False
                case_name = ""

            elif var_menu == "0":
                program_active = False
            else:
                print("Invalid entry, retry!")
                time.sleep(1)

        else:
            print("Invalid entry, retry!")
            time.sleep(1)
        

#######################################################
## Launcher
#######################################################

if __name__ == '__main__':
    main()