# Blockmole

# Imports:
import sqlite3
import time
import os


########################################

# Global variables
main_menu_active = True
database_isloaded = False
database_loaded_name = ""
clear = lambda: os.system("cls")
table_create_name = ""

#########################################

# Functions

"""def get_time():
    time = time.localtime(time.time())
    return time


def casedata_collect():
    sub_menu_add = True
    address_list = []
    while sub_menu_add == True:
        address_sub_list = ["NONE", ]
        clear()
        print("### Adding data ###\n\n")
        address = input("Please enter the address you want to track: ")
        time_added = 0
        has_transaction = "FALSE"
        last_used = 0
        comment = input("Add a comment for this address: ")
        """

def add_data(state):
    if state == True:
        sub_menu_add = True
        address_list = []
        while sub_menu_add == True:
            address_sub_list = []
            clear()
            print("### Adding data ###\n\n")
            address = input("Please enter the address you want to track: ")
            comment = input("Please enter a comment for that address: ")
            address_sub_list.append(address)
            address_sub_list.append(False)
            address_sub_list.append("NULL")
            address_sub_list.append(comment)
            address_list.append(address_sub_list)
            frage = input("Do you want to add another address [0 / 1]?: ")
            if frage == "0":
                sub_menu_add = False
            
        cursor.executemany("""INSERT INTO [%s] VALUES (NULL,?,CURRENT_TIMESTAMP,?,?,?)""" % table_create_name , address_list)
        connect.commit()

    else:
        print("### Please load or create a database first! ###")
    return


#########################################

# Program start


clear()
print("Welcome to Blockmole, a simple Bitcointrackingtool!")

# Main menu

while main_menu_active == True:
    print("\n### MAIN MENU ###")
    if database_isloaded == False:
        print("\n   > Current status: ")
        print("     No casefile loaded. Please create or load a casefile first!")
    else:
        print("\n   > Current status: ")
        print("     Casefile loaded: %s" % database_loaded_name)
    print("\nPlease select a function:\n")
    print(" 1. Case functions: Create / Load / Delete casefiles")
    print(" 2. Instance functions: Add / Edit / Delete case instances")
    print(" 3. Tracking functions: Check for new transactions\n")
    print(" 4. EXIT\n")

    user_choice1 = input("blockmole >> ")
    clear()

    # Databasemenu

    if user_choice1 == "1":

        sub_menu_data = True

        while sub_menu_data == True:

            print("\n### Case functions ### ")
            if database_isloaded == False:
                print("\n   > Current status: ")
                print("     No casefile loaded. Please create or load a casefile first!")
                
            else:
                print("\n   > Current status: ")
                print("     Loaded casefile: %s" % database_loaded_name)
            print("\n1. Show existing casefiles")
            print("2. Create or load a casefile")
            print("3. Unload the database")
            print("4. Delete an existing casefile\n")
            
            print("X. Back to main menu\n")

            user_choice_data = input("blockmole >> ")
            
            clear()

            # Show databases
            
            if user_choice_data == "1":
                files = filter(os.path.isfile, os.listdir(os.curdir))
                files_db = [fi for fi in files if fi.endswith(".db")]
                clear()
                print("\n### Existing casefiles ###\n")
                for i in files_db:
                    print(" - " + str(i))
                print("\n############")

            # Create or load database

            elif user_choice_data == "2":
                if database_isloaded == False:
                    print("\n### Creating or loading a database ###\n")
                    database_create_name = input("Please enter the casenumber for the file to be loaded or created: ")
                    connect = sqlite3.connect(str(database_create_name)+'.db')
                    cursor = connect.cursor()
                    database_isloaded = True
                    time.sleep(1)
                    database_loaded_name = database_create_name
                    print("\n### Database loaded! ###\n")
                    time.sleep(1)
                    clear()
                else:
                    print("### Case already loaded! Please unload the current casefile first! ###")
                    time.sleep(2)
                    clear()

            # Close the connection to the loaded database

            elif user_choice_data == "3":
                if database_isloaded == True:
                    print("\n### Closing connection to database ###")
                    connect.close()
                    database_isloaded = False
                    time.sleep(1)
                    print("\n### Success! ###")
                    time.sleep(1)
                    clear()
                else:
                    print("\n### No connection found ###\n")
                    time.sleep(1)
                    clear()

            # Deleting an existing databasefile

            elif user_choice_data == "4":
                print("\n### Deleting an existing database ###\n")
                sub_menu_delete = True
                while sub_menu_delete == True:
                    try:
                        if database_isloaded == True:
                            print("\n### Closing existing connections to databases first...")
                            time.sleep(1)
                            connect.close()
                            database_isloaded = False
                            print("\n### Connections closed...\n")
                        database_delete_name = input("Please enter the casenumber of the file you want to delete: ")
                        os.remove(str(database_delete_name)+".db")
                        time.sleep(1)
                        print("\n### Case number %s successfully deleted! ###\n" % database_delete_name)
                        time.sleep(1)
                        clear()
                        break
                    except:
                        print("\nFile not existing, please try again\n")
                        time.sleep(1)
                        clear()
                        sub_menu_delete = False  
                
            elif user_choice_data == "X":
                sub_menu_data = False
            else:
                print("Invalid choice!\n")

    # Instance menu

    elif user_choice1 == "2":

        sub_menu_btc = True

        while sub_menu_btc == True:
            print("\n### Instance functions ###")
            if database_isloaded == False:
                print("\n   > Current status: ")
                print("     No casefile loaded. Please create or load a casefile first!")
            else:
                print("\n   > Current status: ")
                print("     Loaded casefile: %s" % database_loaded_name)
            print("\n1. Add a new case instance")
            print("2. Edit an existing case instance")
            print("3. Delete a case instance")
            
            print("\nX. Back to main menu!\n")
            user_choice_btc = input("blockmole >> ")
            
            if user_choice_btc == "1":
                
                if database_isloaded == True:
                    table_create_name = str(input("Please enter your instance number: "))
                    print("\n### Creating a new table...")
                    
                    cursor.execute("""CREATE TABLE IF NOT EXISTS [%s] (
                        address_number INTEGER PRIMARY KEY,
                        address TEXT,
                        date_added TEXT,
                        has_transaction BOOLEAN,
                        last_used FLOAT,
                        comment TEXT);""" % table_create_name)
                    time.sleep(1)
                    print("\n### Table has been successfully created! ###")
                else:
                    print("\n### Load or create a database first! ###")

            elif user_choice_btc == "2":
                add_data(database_isloaded)
                """if database_isloaded == True:
                    sub_menu_add = True
                    address_list = []
                    while sub_menu_add == True:
                        address_sub_list = []
                        clear()
                        print("### Adding data ###\n\n")
                        address = input("Please enter the address you want to track: ")
                        comment = input("Please enter a comment for that address: ")
                        address_sub_list.append(address)
                        #address_sub_list.append(time.time())
                        address_sub_list.append(False)
                        address_sub_list.append("NULL")
                        address_sub_list.append(comment)
                        address_list.append(address_sub_list)
                        frage = input("Do you want to add another address [0 / 1]?: ")
                        if frage == "0":
                            sub_menu_add = False
                        
                    cursor.executemany(""" """INSERT INTO [%s] VALUES (NULL,?,CURRENT_TIMESTAMP,?,?,?)""" """ % table_create_name , address_list)
                    connect.commit()

                else:
                    print("### Please load or create a database first! ###")  """

            elif user_choice_btc == "X":
                print("\n Back to main menu!\n")
                sub_menu_btc = False
        
            else:
                print("Invalid choice!")

    # Trackingfunctionality

    elif user_choice1 == "3":

        print("### Trackingfunctions ###")
        sub_menu_track = True

        while sub_menu_track == True:
            print("1. Back to main menu!")
            user_choice_track = input("Please enter: ")
            if user_choice_track == "1":
                print("\n Back to main menu!\n")
                sub_menu_track = False
            else:
                print("Invalid choice!")

    elif user_choice1 == "4":
        print("##### EXITING #####")
        time.sleep(1)
        
        main_menu_active = False

    else:
        print("Invalid choice!")



