import sys

sys.path.append('Modules')
import os
from getpass import getpass
import namesearch
from namesearch import *
import phoneinfo
from phoneinfo import *
import tracer
from tracer import *
import os
import time
from colorama import Fore, Style
import getpass
import mysql.connector
import psycopg2

import sys
import os
import time
from colorama import Fore, Style
import getpass
import json
import mysql.connector
import psycopg2

USER_DATA_FILE = "users.json"
DATABASE_CONFIG_FILE = "database_config.json"
CURRENT_DB_CONNECTION = None
LOGGED_IN_USER = None


def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def load_users():
    """Loads user data from the JSON file."""
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(Fore.YELLOW + "Warning: Could not decode user data. Starting with an empty user list." + Style.RESET_ALL)
        return {}


def save_users(users):
    """Saves user data to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)


def load_database_config():
    """Loads database configuration from the JSON file."""
    try:
        with open(DATABASE_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(Fore.YELLOW + f"Warning: Configuration file '{DATABASE_CONFIG_FILE}' not found." + Style.RESET_ALL)
        return {}
    except json.JSONDecodeError:
        print(
            Fore.YELLOW + f"Warning: Configuration file '{DATABASE_CONFIG_FILE}' contains invalid JSON." + Style.RESET_ALL)
        return {}


def connect_to_db(db_config):
    """Connects to the specified database based on the configuration."""
    db_type = db_config.get("type")
    host = db_config.get("host")
    user = db_config.get("user")
    password = db_config.get("password")
    database = db_config.get("database")

    try:
        if db_type == "mysql":
            mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
            print(Fore.GREEN + f"Connected to MySQL: {database}@{host}" + Style.RESET_ALL)
            return mydb
        elif db_type == "postgresql":
            conn = psycopg2.connect(host=host, database=database, user=user, password=password)
            print(Fore.GREEN + f"Connected to PostgreSQL: {database}@{host}" + Style.RESET_ALL)
            return conn
        else:
            print(Fore.RED + f"Error: Database type '{db_type}' not supported." + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"Error connecting to the database: {e}" + Style.RESET_ALL)
        return None


def create_account():
    """Creates a new user account."""
    users = load_users()
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "Create New Account" + Style.RESET_ALL)
    print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
    print()
    username = input(Fore.YELLOW + "Enter a new username: " + Style.RESET_ALL).strip()
    if not username:
        print(Fore.RED + "Username cannot be empty." + Style.RESET_ALL)
        time.sleep(1)
        return False
    if username in users:
        print(Fore.RED + f"Username '{username}' already exists." + Style.RESET_ALL)
        time.sleep(1)
        return False

    while True:
        password = getpass.getpass(Fore.YELLOW + f"Set password for '{username}': " + Style.RESET_ALL)
        confirm_password = getpass.getpass(Fore.YELLOW + f"Confirm password for '{username}': " + Style.RESET_ALL)
        if password == confirm_password:
            users[username] = password  # In a real application, hash the password!
            save_users(users)
            print(Fore.GREEN + f"Account created successfully for '{username}'." + Style.RESET_ALL)
            time.sleep(1)
            return True
        else:
            print(Fore.RED + "Passwords do not match. Please try again." + Style.RESET_ALL)
            time.sleep(1)
        print("-" * 30)


def login():
    """Handles the login process."""
    users = load_users()
    clear_screen()

    print(Fore.CYAN + Style.BRIGHT + "Login to Andromeda" + Style.RESET_ALL)
    print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
    print()

    username = input(Fore.YELLOW + "Username: " + Style.RESET_ALL).strip()
    password = input(Fore.YELLOW + "Password: " + Style.RESET_ALL)

    if username in users and users[username] == password:
        print(Fore.GREEN + "Login successful!" + Style.RESET_ALL)
        time.sleep(1)
        return True
    else:
        print(Fore.RED + "Login failed. Incorrect username or password." + Style.RESET_ALL)
        time.sleep(1)
        return False

def login_menu():
    """Presents the login menu with options to login or create an account."""

    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "Welcome to Andromeda" + Style.RESET_ALL)
        print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
        print(Fore.BLUE + '''
        [1] Login
        [2] Create Account
        [3] Exit
        ''' + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice == '1':
            if login() is True:
                print(Fore.GREEN + "\nAccess granted. Proceeding to the main application..." + Style.RESET_ALL)
                time.sleep(1)
                return True  # Login successful, return True to proceed
            else:
                print(Fore.RED + "\nLogin failed. Please try again or create an account." + Style.RESET_ALL)
                time.sleep(1)
                return False
        elif choice == '2':
            create_account()
        elif choice == '3':
            print(Fore.YELLOW + "Exiting Andromeda." + Style.RESET_ALL)
            return False  # Indicate exit
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
            time.sleep(1)


def choose_database():
    """Allows the user to choose a database from the configuration."""
    config = load_database_config()
    if not config:
        return None

    db_options = list(config.keys())
    if not db_options:
        print(Fore.YELLOW + "Warning: No database configurations found." + Style.RESET_ALL)
        return None

    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "Choose Database" + Style.RESET_ALL)
        print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
        for i, db_name in enumerate(db_options):
            print(Fore.BLUE + f"[{i + 1}] {db_name}" + Style.RESET_ALL)
        print(Fore.YELLOW + "[B] Back to Setup Menu" + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip().lower()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(db_options):
                selected_db_name = db_options[index]
                return config[selected_db_name]
            else:
                print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
                time.sleep(1)
        elif choice == 'b':
            return None
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            time.sleep(1)


def database_menu():
    """Menu specifically for database connection."""
    global CURRENT_DB_CONNECTION
    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "Database Setup" + Style.RESET_ALL)
        print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
        if CURRENT_DB_CONNECTION:
            print(
                Fore.GREEN + f"Connected to: {CURRENT_DB_CONNECTION.get_server_info() if hasattr(CURRENT_DB_CONNECTION, 'get_server_info') else 'Database'}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Not connected to any database." + Style.RESET_ALL)
        print(Fore.BLUE + '''
        [1] Connect to Database
        [2] Disconnect Database
        [3] Back to Setup Menu
        ''' + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice == '1':
            db_config = choose_database()
            if db_config:
                CURRENT_DB_CONNECTION = connect_to_db(db_config)
        elif choice == '2':
            if CURRENT_DB_CONNECTION:
                CURRENT_DB_CONNECTION.close()
                CURRENT_DB_CONNECTION = None
                print(Fore.YELLOW + "Disconnected from the database." + Style.RESET_ALL)
                time.sleep(1)
            else:
                print(Fore.YELLOW + "Not connected to any database." + Style.RESET_ALL)
                time.sleep(1)
        elif choice == '3':
            return True  # Go back to setup menu
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            time.sleep(1)


def more_menu():
    """Placeholder for a 'more' menu."""
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "More Options" + Style.RESET_ALL)
    print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
    print(Fore.BLUE + '''
        [1] Option A
        [2] Option B
        [3] Back to Setup Menu
        ''' + Style.RESET_ALL)
    choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
    if choice == '3':
        return True
    else:
        print(Fore.YELLOW + "This option is a placeholder." + Style.RESET_ALL)
        input("Press Enter to return to Setup Menu...")
        return False

def test_menu():
    return andro_menu()

def main_starter_menu():
    """The main setup menu."""
    while True:
        clear_screen()
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                             SETUP MENU                                           ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
           [1] Login                         
           [2] Data Base Setup                  
           [3] More Options
           [4] Test

           [99] Exit             
            ''' + Style.RESET_ALL)
        print(Fore.WHITE)
        print('------------------------------------------------------------------------------')
        try:
            choice = input(Fore.RED + "root" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "DRF-Machina" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                if login_menu():
                    print(Fore.GREEN + "\nReturning to Setup Menu after login." + Style.RESET_ALL)
                    input('Press Enter to continue...')
            elif choice == "2":
                if database_menu():
                    print(Fore.GREEN + "\nReturning to Setup Menu after database setup." + Style.RESET_ALL)
                    input('Press Enter to continue...')
            elif choice == "3":
                if more_menu():
                    print(Fore.GREEN + "\nReturning to Setup Menu after more options." + Style.RESET_ALL)
                    input('Press Enter to continue...')
            elif choice == "4":
                if test_menu():
                    print(Fore.GREEN + "\n Bypass all, connection to Andromeda" + Style.RESET_ALL)
                    input('Press Enter to continue...')
            elif choice == "99":
                print(Fore.YELLOW + "Exiting Andromeda Setup." + Style.RESET_ALL)
                sys.exit()
            else:
                print(Fore.RED + '  Incorrect choice ' + Style.RESET_ALL)
                print('\r')
                input('Press Enter to return to Setup Menu...')
        except KeyboardInterrupt:
            print('\n' + Fore.YELLOW + "Exiting Andromeda Setup." + Style.RESET_ALL)
            sys.exit()

if __name__ == "__main__":
    main_starter_menu()
def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_database_interaction(db_connection):
    """Example function to interact with the connected database."""
    cursor = db_connection.cursor()
    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "Database Interaction" + Style.RESET_ALL)
        print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
        print(Fore.BLUE + '''
        [1] List Data (Example)
        [2] Perform Action (Example)
        [3] Disconnect and Back to Main Menu
        ''' + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice == '1':
            try:
                cursor.execute("SELECT * FROM your_table_name LIMIT 10") # Replace with your actual table
                results = cursor.fetchall()
                print(Fore.GREEN + "\n--- Data ---" + Style.RESET_ALL)
                for row in results:
                    print(row)
                input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error fetching data: {e}" + Style.RESET_ALL)
                input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
        elif choice == '2':
            print(Fore.YELLOW + "Performing action on the database..." + Style.RESET_ALL)
            time.sleep(1)
            # Add your database modification code here (INSERT, UPDATE, DELETE)
            # Remember to commit changes: db_connection.commit()
            input(Fore.YELLOW + "Action performed (placeholder). Press Enter to continue..." + Style.RESET_ALL)
        elif choice == '3':
            break
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            time.sleep(1)

    cursor.close()
    return True

def database_menu():
    """Menu specifically for database connection and interaction."""
    global CURRENT_DB_CONNECTION
    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "Database Management" + Style.RESET_ALL)
        print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
        if CURRENT_DB_CONNECTION:
            print(Fore.GREEN + "Connected to a database." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Connect to your database." + Style.RESET_ALL)
        print(Fore.BLUE + '''
        [1] Connect to Database
        [2] Interact with Database (if connected)
        [3] Back to Main Menu
        ''' + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice == '1':
            db_config = choose_database()
            if db_config:
                CURRENT_DB_CONNECTION = connect_to_db(db_config)
        elif choice == '2':
            if CURRENT_DB_CONNECTION:
                handle_database_interaction(CURRENT_DB_CONNECTION)
            else:
                print(Fore.YELLOW + "Please connect to a database first." + Style.RESET_ALL)
                time.sleep(1)
        elif choice == '3':
            if CURRENT_DB_CONNECTION:
                CURRENT_DB_CONNECTION.close()
                CURRENT_DB_CONNECTION = None
                print(Fore.YELLOW + "Disconnected from the database." + Style.RESET_ALL)
                time.sleep(1)
            return True
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            time.sleep(1)

if __name__ == "__main__":
    database_menu()

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_users():
    """Loads user data from the JSON file."""
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(Fore.YELLOW + "Warning: Could not decode user data. Starting with an empty user list." + Style.RESET_ALL)
        return {}

def save_users(users):
    """Saves user data to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def create_account():
    """Creates a new user account."""
    users = load_users()
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "Create New Account" + Style.RESET_ALL)
    print(Fore.WHITE + "-------------------------" + Style.RESET_ALL)
    print()
    username = input(Fore.YELLOW + "Enter a new username: " + Style.RESET_ALL).strip()
    if not username:
        print(Fore.RED + "Username cannot be empty." + Style.RESET_ALL)
        time.sleep(1)
        return False
    if username in users:
        print(Fore.RED + f"Username '{username}' already exists." + Style.RESET_ALL)
        time.sleep(1)
        return False

    while True:
        password = getpass.getpass(Fore.YELLOW + f"Set password for '{username}': " + Style.RESET_ALL)
        confirm_password = input(Fore.YELLOW + f"Confirm password for '{username}': " + Style.RESET_ALL)
        if password == confirm_password:
            users[username] = password  # In a real application, hash the password!
            save_users(users)
            print(Fore.GREEN + f"Account created successfully for '{username}'." + Style.RESET_ALL)
            time.sleep(1)
            return True
        else:
            print(Fore.RED + "Passwords do not match. Please try again." + Style.RESET_ALL)
            time.sleep(1)
        print("-" * 30)

if __name__ == "__main__":
    login_successful = login_menu()
    if login_successful:
        time.sleep(2)
        # Place your main application code here
        print(Fore.CYAN + Style.BRIGHT + "Andromeda is loading" + Style.RESET_ALL)
        time.sleep(5)
        print(Fore.WHITE + "Welcome, Sir! Andromeda the greatest is ready1!" + Style.RESET_ALL)

    else:
        print(Fore.YELLOW + "\nExiting the application." + Style.RESET_ALL)
        exit()
print('\r')
print(Fore.RED + '''
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ TO
''')

os.system('cls' if os.name == 'nt' else 'clear')
time.sleep(2)

def andro_menu():
    print(Fore.RED + "    _    _   _ ____  ____   ___  __  __ _____ ____    _    ")
    print(Fore.RED + "   / \\  | \\ | |  _ \\|  _ \\ / _ \\|  \\/  | ____|  _ \\  / \\   ")
    print(Fore.RED + "  / _ \\ |  \\| | | | | |_) | | | | |\\/| |  _| | | | |/ _ \\  ")
    print(Fore.BLUE + " / ___ \\| |\\  | |_| |  _ <| |_| | |  | | |___| |_| / ___ \\ ")
    print(Fore.BLUE + "/_/   \\_\\_| \\_|____/|_| \\_\\\\___/|_|  |_|_____|____/_/   \\_\\ Framework v0.1" + Style.RESET_ALL)
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                 MENU                                           ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
       [1] Osint                     [5] Steganography     
       [2] Forensic                  [6] Misc
       [3] Cracking                  [7] Reverse 
       [4] Scripting                 [8] Web 
        ''')
    print(Fore.WHITE)
    print('------------------------------------------------------------------------------')
    print(Fore.LIGHTBLACK_EX + '''                 Make by Ake AshK"3NaZz TBE ~ ''' + Fore.WHITE)
    print('------------------------------------------------------------------------------')
    try:
        choice = input(Fore.RED + "root" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            menu_osint()
            input('enter to main menu ...')
            andro_menu()
        elif choice == "2":
            menu_forensic()
            input('enter to main menu ...')
            andro_menu()
        elif choice == "3":
            menu_cracking()
            input('enter to main menu')
            andro_menu()
        elif choice == "4":
            menu_scripting()
            input('enter to main menu')
            andro_menu()
        elif choice == "5":
            menu_stega()
            input('enter to main menu')
            andro_menu()
        elif choice == "6":
            menu_misc()
            input('enter to main menu')
            andro_menu()
        elif choice == "7":
            menu_reverse()
            input('enter to main menu')
            andro_menu()
        elif choice == "8":
            menu_web()
            input('enter to main menu')
            andro_menu()
        else:
            print('  incorrect choice ')
            print('\r')
            input('enter to main menu ...')
            andro_menu()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


## Menu settings
# OSINT menu

def menu_osint():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                    OSINT                                                ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] Name Searching            [4] Email Searching  --OFF--
    [2] Phone Directory           [5] Web Analyzer     --OFF--
    [3] IP Information            [6] Meta-data Analyzer --OFF--     

    [99] Main menu      
     ''')
    print('\r')
    try:
        choice = input(Fore.RED + "osint" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            name_search()
            input('enter to main menu ...')
            menu_osint()
        elif choice == "2":
            phone()
            input('enter to main menu ...')
            menu_osint()
        elif choice == "3":
            ip()
            input('enter to main menu')
            menu_osint()
        elif choice == "4":
            email_harper()
            input('enter to main menu')
            menu_osint()
        elif choice == "5":
            web_scrap()
            input('enter to main menu')
            menu_osint()
        elif choice == "6":
            meta_scan()
            input('enter to main menu')
            menu_osint()
        elif choice == "99":
            return andro_menu()
        else:
            print('  incorrect choice ')
            print('\r')
            input('enter to main menu ...')
            andro_menu()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# Forensic menu settings

def menu_forensic():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                  FORENSIC                                                ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
            [1] MIG                       [4] TSK (The Sleuth Kit)
            [2] GRR                       [5] Caine
            [3] Volatility                [6] Bulk Extractor


            [99] Main menu
     ''')
    print('\r')
    try:
        choice = input(Fore.RED + "forensic" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            mig()
            input('enter to main menu ...')
            menu_forensic()
        elif choice == "2":
            grr()
            input('enter to main menu ...')
            menu_forensic()
        elif choice == "3":
            vol()
            input('enter to main menu')
            menu_forensic()
        elif choice == "99":
            return andro_menu()
        else:
            print('  incorrect choice ')
            print('\r')
            input('enter to main menu ...')
            andro_menu()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# Crypto menu
def menu_cracking():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(
            Fore.WHITE + '                                    Cracking                                               ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')

        print(Fore.BLUE + '''
        [1] Password                  [4] System
        [2] Software                  [5] Web
        [3] Network                   [6] Cryptography

        [99] Main menu
         ''')

        print('\r')
        try:
            choice = input(
                Fore.RED + "cracking" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                password_submenu()  # Call password cracking submenu
            elif choice == "2":
                software_submenu()  # Call software cracking submenu
            elif choice == "3":
                network_submenu()  # Call network cracking submenu
            elif choice == "4":
                system_submenu()
            elif choice == "5":
                web_submenu()
            elif choice == "6":
                crypto_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to Cracking menu...')
        except KeyboardInterrupt:
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to cracking menu...')

# Submenu definitions
def password_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Dictionary                [2] Brute force
        [3] Rainbow table           

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Dictionary cracking...")
        elif choice == "2":
            print("Brute force cracking...")
        elif choice == "3":
            print("Rainbow table cracking...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")

def software_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Keygen                    [2] Patching
        [3] Reverse engineering       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Key generation...")
        elif choice == "2":
            print("Patching...")
        elif choice == "3":
            print("Reverse engineering...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")

def network_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Sniffing                  [2] Spoofing
        [3] DoS attack                

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Network sniffing...")
        elif choice == "2":
            print("Address spoofing...")
        elif choice == "3":
            print("Denial of service attack...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")

def system_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Vuln exploit                 [2] Rooting
        [3] Privilege escalation      

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Vulnerability exploitation...")
        elif choice == "2":
            print("Rooting...")
        elif choice == "3":
            print("Privilege escalation...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")

def web_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] SQL Injection               [2] XSS
        [3] CSRF                        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("SQL injection...")
        elif choice == "2":
            print("XSS...")
        elif choice == "3":
            print("CSRF...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")

def crypto_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Private key theft           [2] 51% attack
        [3] Phishing                  

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Private key theft...")
        elif choice == "2":
            print("51% attack...")
        elif choice == "3":
            print("Phishing...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")

## Scripting menu settings
def menu_scripting():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                   Scripting                                              ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] System            [5] Security
        [2] Web               [6] Game
        [3] Network           [7] Data     
        [4] Automation        [8] Application

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(
                Fore.RED + "scripting" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                system_scripting_submenu()
            elif choice == "2":
                web_scripting_submenu()
            elif choice == "3":
                network_scripting_submenu()
            elif choice == "4":
                automation_scripting_submenu()
            elif choice == "5":
                security_scripting_submenu()
            elif choice == "6":
                game_scripting_submenu()
            elif choice == "7":
                data_scripting_submenu()
            elif choice == "8":
                application_scripting_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to scripting menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to scripting menu...')

def system_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] File management         [2] Process control
        [3] System monitoring       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("File management scripting...")
        elif choice == "2":
            print("Process control scripting...")
        elif choice == "3":
            print("System monitoring scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")

def web_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Web scraping            [2] API interaction
        [3] Dynamic content gen.    

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Web scraping scripting...")
        elif choice == "2":
            print("API interaction scripting...")
        elif choice == "3":
            print("Dynamic content generation scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")

def network_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Network scanning        [2] Packet analysis
        [3] Socket programming      

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Network scanning scripting...")
        elif choice == "2":
            print("Packet analysis scripting...")
        elif choice == "3":
            print("Socket programming scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")

def automation_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Task scheduling         [2] UI automation
        [3] Data processing         

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Task scheduling scripting...")
        elif choice == "2":
            print("UI automation scripting...")
        elif choice == "3":
            print("Data processing automation scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def security_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Vulnerability scanning      [2] Log analysis
        [3] Intrusion detection     

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Vulnerability scanning scripting...")
        elif choice == "2":
            print("Log analysis scripting...")
        elif choice == "3":
            print("Intrusion detection scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def game_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Game logic              [2] Modding tools
        [3] AI behaviors           

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Game logic scripting...")
        elif choice == "2":
            print("Modding tools scripting...")
        elif choice == "3":
            print("AI behaviors scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def data_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Data parsing            [2] Data transformation
        [3] Data visualization      

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Data parsing scripting...")
        elif choice == "2":
            print("Data transformation scripting...")
        elif choice == "3":
            print("Data visualization scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def application_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Plugin development      [2] Macro creation
        [3] API usage             

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Plugin development scripting...")
        elif choice == "2":
            print("Macro creation scripting...")
        elif choice == "3":
            print("API usage scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


## Steganography menu settings
## Stegano submenu settings
def menu_stega():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(
            Fore.WHITE + '                                   Steganography                                             ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Images                    [4] Text
        [2] Audio                     [5] Network
        [3] Video                     [6] File System     

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(
                Fore.RED + "steganography" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                image_stega_submenu()
            elif choice == "2":
                audio_stega_submenu()
            elif choice == "3":
                video_stega_submenu()
            elif choice == "4":
                text_stega_submenu()
            elif choice == "5":
                network_stega_submenu()
            elif choice == "6":
                filesystem_stega_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to steganography menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to steganography menu...')


def image_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] LSB Embedding             [2] Pixel Manipulation
        [3] Frequency Domain          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("LSB embedding steganography...")
        elif choice == "2":
            print("Pixel manipulation steganography...")
        elif choice == "3":
            print("Frequency domain steganography...")
        elif choice == "99":
            return
        else:
            print("Invalid choice.")


def audio_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] LSB Embedding             [2] Echo Hiding
        [3] Phase Coding              

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("LSB embedding audio steganography...")
        elif choice == "2":
            print("Echo hiding audio steganography...")
        elif choice == "3":
            print("Phase coding audio steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def video_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Frame Embedding           [2] Motion Vectors
        [3] DCT Techniques            

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Frame embedding video steganography...")
        elif choice == "2":
            print("Motion vectors video steganography...")
        elif choice == "3":
            print("DCT techniques video steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def text_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Line Shifting             [2] Word Shifting
        [3] Character Coding          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Line shifting text steganography...")
        elif choice == "2":
            print("Word shifting text steganography...")
        elif choice == "3":
            print("Character coding text steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def network_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Protocol Fields           [2] Packet Timing
        [3] IP Header Stego           

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Protocol fields network steganography...")
        elif choice == "2":
            print("Packet timing network steganography...")
        elif choice == "3":
            print("IP header steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def filesystem_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Alternate Data Streams    [2] Hidden Partitions
        [3] File Slack Space          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Alternate data streams filesystem steganography...")
        elif choice == "2":
            print("Hidden partitions filesystem steganography...")
        elif choice == "3":
            print("File slack space filesystem steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


## Misc menu settings

def menu_misc():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                   Misc                                             ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1]  File manipulation                    [6]  Hardware interact 
        [2]  Data conversion                      [7]  Encoding / Decoding
        [3]  System utilities                     [8]  Randomization    
        [4]  Text processing                      [9]  Mathematics tools
        [5]  Web scraping                         [10] Automation tools    

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(Fore.RED + "misc" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                file_manipulation_submenu()
            elif choice == "2":
                data_conversion_submenu()
            elif choice == "3":
                system_utilities_submenu()
            elif choice == "4":
                text_processing_submenu()
            elif choice == "5":
                web_scraping_submenu()
            elif choice == "6":
                hardware_interaction_submenu()
            elif choice == "7":
                encoding_decoding_submenu()
            elif choice == "8":
                randomization_submenu()
            elif choice == "9":
                math_tools_submenu()
            elif choice == "10":
                automation_tools_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to misc menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to misc menu...')


def file_manipulation_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] File renaming             [2] File copying
        [3] File deletion             

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("File renaming...")
        elif choice == "2":
            print("File copying...")
        elif choice == "3":
            print("File deletion...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def data_conversion_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] CSV to JSON                 [2] JSON to XML
        [3] Image format conversion   

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("CSV to JSON conversion...")
        elif choice == "2":
            print("JSON to XML conversion...")
        elif choice == "3":
            print("Image format conversion...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def system_utilities_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Process monitoring        [2] Disk usage analysis
        [3] System info retrieval     

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Process monitoring...")
        elif choice == "2":
            print("Disk usage analysis...")
        elif choice == "3":
            print("System info retrieval...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def text_processing_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Text parsing              [2] Text formatting
        [3] Regular expressions       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Text parsing...")
        elif choice == "2":
            print("Text formatting...")
        elif choice == "3":
            print("Regular expressions...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def web_scraping_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] HTML parsing              [2] Data extraction
        [3] Web page crawling         

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("HTML parsing...")
        elif choice == "2":
            print("Data extraction...")
        elif choice == "3":
            print("Web page crawling...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def hardware_interaction_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Serial communication      [2] GPIO control
        [3] USB device interaction    

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Serial communication...")
        elif choice == "2":
            print("GPIO control...")
        elif choice == "3":
            print("USB device interaction...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def encoding_decoding_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Base64 encoding           [2] URL encoding
        [3] Hexadecimal conversion    

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Base64 encoding...")
        elif choice == "2":
            print("URL encoding...")
        elif choice == "3":
            print("Hexadecimal conversion...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def randomization_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Random number generation    [2] Random string generation
        [3] Data shuffling            

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Random number generation...")
        elif choice == "2":
            print("Random string generation...")
        elif choice == "3":
            print("Data shuffling...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def math_tools_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Statistical calculations    [2] Mathematical functions
        [3] Matrix operations        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Statistical calculations...")
        elif choice == "2":
            print("Mathematical functions...")
        elif choice == "3":
            print("Matrix operations...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def automation_tools_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Task scheduling           [2] Script automation
        [3] Workflow automation       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Task scheduling...")
        elif choice == "2":
            print("Script automation...")
        elif choice == "3":
            print("Workflow automation...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


## Reverse menu settings

def menu_reverse():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                  Reverse                                            ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Software                  [5] Game
        [2] Hardware                  [6] Firmware
        [3] Network protocol          [7] Mobile application     
        [4] Malware                   [8] Web application


        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(
                Fore.RED + "reverse" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                software_reverse_submenu()
            elif choice == "2":
                hardware_reverse_submenu()
            elif choice == "3":
                network_protocol_reverse_submenu()
            elif choice == "4":
                malware_reverse_submenu()
            elif choice == "5":
                game_reverse_submenu()
            elif choice == "6":
                firmware_reverse_submenu()
            elif choice == "7":
                mobile_application_reverse_submenu()
            elif choice == "8":
                web_application_reverse_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to reverse menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to reverse menu...')


def software_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Static analysis           [2] Dynamic analysis
        [3] Disassembly               [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Static software reverse engineering...")
        elif choice == "2":
            print("Dynamic software reverse engineering...")
        elif choice == "3":
            print("Software disassembly...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def hardware_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Circuit analysis          [2] Bus analysis
        [3] Component analysis        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Circuit analysis hardware reverse engineering...")
        elif choice == "2":
            print("Bus analysis hardware reverse engineering...")
        elif choice == "3":
            print("Component analysis hardware reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def network_protocol_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Packet capture analysis   [2] Protocol dissection
        [3] State machine analysis    [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Packet capture analysis network protocol reverse engineering...")
        elif choice == "2":
            print("Protocol dissection network protocol reverse engineering...")
        elif choice == "3":
            print("State machine analysis network protocol reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def malware_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Static malware analysis   [2] Dynamic malware analysis
        [3] Behavioral analysis       [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Static malware reverse engineering...")
        elif choice == "2":
            print("Dynamic malware reverse engineering...")
        elif choice == "3":
            print("Malware behavioral analysis...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def game_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Game logic analysis       [2] Asset extraction
        [3] Game engine analysis      [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Game logic reverse engineering...")
        elif choice == "2":
            print("Game asset extraction...")
        elif choice == "3":
            print("Game engine reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def firmware_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Firmware extraction       [2] Firmware analysis
        [3] ROM analysis              [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Firmware extraction...")
        elif choice == "2":
            print("Firmware analysis...")
        elif choice == "3":
            print("ROM analysis...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def mobile_application_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] APK/IPA analysis          [2] Dynamic analysis
        [3] Code decompilation        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("APK/IPA analysis mobile application reverse engineering...")
        elif choice == "2":
            print("Dynamic analysis mobile application reverse engineering...")
        elif choice == "3":
            print("Mobile application code decompilation...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def web_application_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Client-side analysis      [2] Server-side analysis
        [3] API analysis              [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Client-side web application reverse engineering...")
        elif choice == "2":
            print("Server-side web application reverse engineering...")
        elif choice == "3":
            print("API web application reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


## Web menu settings

def menu_web():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                   Web                                              ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Injection SQL                                [8] Directory traversal
        [2] Cross-Site Scripting (XSS)                   [9] Remote Code Execution (RCE)
        [3] Cross-Site Request Forgery (CSRF)            [10] Web Shells     
        [4] Authentication Attacks                       [11] Clickjacking
        [5] Session Hijacking                            [12] MitM Attacks
        [6] DoS/DDoS Attacks                             [13] Web Defacement
        [7] File Inclusion                               [14] Phishing

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(Fore.RED + "web" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                sql_injection_submenu()
            elif choice == "2":
                xss_submenu()
            elif choice == "3":
                csrf_submenu()
            elif choice == "4":
                authentication_attacks_submenu()
            elif choice == "5":
                session_hijacking_submenu()
            elif choice == "6":
                dos_ddos_submenu()
            elif choice == "7":
                file_inclusion_submenu()
            elif choice == "8":
                directory_traversal_submenu()
            elif choice == "9":
                rce_submenu()
            elif choice == "10":
                web_shells_submenu()
            elif choice == "11":
                clickjacking_submenu()
            elif choice == "12":
                mitm_attacks_submenu()
            elif choice == "13":
                web_defacement_submenu()
            elif choice == "14":
                phishing_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to web menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to web menu...')


def sql_injection_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Union-based SQLi         [2] Error-based SQLi
        [3] Blind SQLi               

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Union-based SQL injection...")
        elif choice == "2":
            print("Error-based SQL injection...")
        elif choice == "3":
            print("Blind SQL injection...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def xss_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Reflected XSS              [2] Stored XSS
        [3] DOM-based XSS              

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Reflected XSS...")
        elif choice == "2":
            print("Stored XSS...")
        elif choice == "3":
            print("DOM-based XSS...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def csrf_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] GET-based CSRF             [2] POST-based CSRF
        [3] Cookie-based CSRF          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("GET-based CSRF...")
        elif choice == "2":
            print("POST-based CSRF...")
        elif choice == "3":
            print("Cookie-based CSRF...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def authentication_attacks_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Brute-force attacks        [2] Dictionary attacks
        [3] Credential stuffing        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Brute-force authentication attacks...")
        elif choice == "2":
            print("Dictionary authentication attacks...")
        elif choice == "3":
            print("Credential stuffing attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def session_hijacking_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Session fixation           [2] Session stealing
        [3] Cookie manipulation        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Session fixation attacks...")
        elif choice == "2":
            print("Session stealing attacks...")
        elif choice == "3":
            print("Cookie manipulation attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def dos_ddos_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] SYN flood attacks          [2] HTTP flood attacks
        [3] UDP flood attacks          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("SYN flood attacks...")
        elif choice == "2":
            print("HTTP flood attacks...")
        elif choice == "3":
            print("UDP flood attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def file_inclusion_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Local file inclusion (LFI)  [2] Remote file inclusion (RFI)

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Local file inclusion (LFI) attacks...")
        elif choice == "2":
            print("Remote file inclusion (RFI) attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def directory_traversal_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Relative path traversal    [2] Absolute path traversal

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Relative path traversal attacks...")
        elif choice == "2":
            print("Absolute path traversal attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def rce_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Command injection          [2] Code injection

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Command injection attacks...")
        elif choice == "2":
            print("Code injection attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def web_shells_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Uploading web shells        [2] Using web shells

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Uploading web shells...")
        elif choice == "2":
            print("Using web shells...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def clickjacking_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Iframe clickjacking        [2] CSS clickjacking

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Iframe clickjacking attacks...")
        elif choice == "2":
            print("CSS clickjacking attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def mitm_attacks_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] ARP poisoning              [2] DNS spoofing
        [3] SSL stripping             

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("ARP poisoning attacks...")
        elif choice == "2":
            print("DNS spoofing attacks...")
        elif choice == "3":
            print("SSL stripping attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def web_defacement_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] File replacement           [2] Database modification

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Web defacement file replacement...")
        elif choice == "2":
            print("Web defacement database modification...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def phishing_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Email phishing             [2] Website phishing

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Email phishing attacks...")
        elif choice == "2":
            print("Website phishing attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")

andro_menu()