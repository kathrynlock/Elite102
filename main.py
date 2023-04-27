import tkinter as tk
import PyPDF2
import mysql.connector
from PIL import Image, ImageTk

def connect_to_db():
    return mysql.connector.connect(
        user = 'root', 
        database = 'k_bank', 
        password = 'Disney06!')

def execute_query(connection, query):
    cursor = connection.cursor()

    cursor.execute(query)
    connection.commit()

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    result = cursor.fetchone()
    balance = result[0]
    return balance

#checks pin to account number entered
def login(connection):
    acc_num = input("Please enter your account number: ")
    try:
        read_query(connection, "SELECT accountNum from accounts where accountNum = " + acc_num)
    except:
        while True:
            acc_num = input("That account number is invalid. Please enter a different account number or enter CREATE to create a new account. ")
            if acc_num == "CREATE":
                create_account(connection)
                break
            else:
                try:
                    read_query(connection, "SELECT accountNum from accounts WHERE accountNum = " + acc_num)
                    break
                except:
                    pass
    pin = input("Please enter your PIN: ")
    account_pin = read_query(connection, "SELECT pin from accounts WHERE accountNum = " + acc_num)
    while pin != account_pin:
        pin = input("That pin was incorrect, please try again. ")
    print("Success!")
    return acc_num

def check_balance(acc_num):
    checkBalQuery = f"SELECT balance FROM accounts WHERE accountNum = {acc_num}"
    return checkBalQuery

def display_balance(connection, acc_num):
    balanceQuery = check_balance(acc_num)
    
    balance = read_query(connection, balanceQuery)
    print("Your account balance is $" + "%.2f" % (balance / 100))

def make_desposit(connection, acc_num):
    #input from GUI
    amount = int(input("How much money would you like to deposit? "))
    balance = read_query(connection, check_balance(acc_num))
    despositQuery = f"UPDATE accounts SET balance = {balance + (amount * 100)} WHERE accountNum = {acc_num}"
    execute_query(connection, despositQuery)

def make_withdraw(connection, acc_num):
    #input from GUI
    amount = int(input("How much money would you like to withdraw? "))
    balance = read_query(connection, check_balance(acc_num))
    withdrawQuery = f"UPDATE accounts SET balance = {balance - (amount * 100)} WHERE accountNum = {acc_num}"
    execute_query(connection, withdrawQuery)

def create_account(connection):
    name = input("What is your name? ")
    dob = input("What is your date of birth (MM/DD/YYYY)? ")
    pin = input("What would you like to set your PIN to? ")

    createQuery = f"INSERT INTO accounts (pin, name, dob, balance) VALUES ({pin}, \"{name}\", \"{dob}\", 0)"
    execute_query(connection, createQuery)

    #add a thing where it tells the user their account number after the acc is created
def close_account(connection, acc_num):
    confirm_pin = input("Please confirm you would like to close your account by entering your PIN")
    #checks to make sure pin is correct for account that is logged in

    closeQuery = f"DELETE from accounts WHERE accountNum = {acc_num}"
    execute_query(connection, closeQuery)

def modify_account(connection, acc_num):
    # can modify name, dob, or pin
    modify_element = input("What would you like to modify? Your account name, dob, or pin?")
    change_to = input("What would you like to change your", modify_element, "to?")
    modifyQuery = f"UPDATE accounts SET {modify_element} = {change_to} WHERE accountNum = {acc_num}"
    execute_query(connection, acc_num)

def menu():
    print("What would you like to do?")
    print('''
    1. Check Balance
    2. Deposit Money
    3. Withdraw Money
    4. Edit Your Account
    ''')
    choice = input()
    return choice

if __name__ == '__main__':
    connection = connect_to_db()
    cursor = connection.cursor()    

    intro = input("Would you like to LOGIN or MAKE an account? ").upper()
    if intro == "LOGIN": 
        account_num = login(connection)
    else:
        create_account(connection)
    
    choice = int(menu())
    make_choice = True
    while make_choice:
        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            pass

    connection.close() 
    '''
    root = tk.Tk()
    root.geometry("600x400")
    frame = tk.Frame(root, height=400, width=700, bg="#52489C")
    frame.pack()

    #instructions 
    instructions = tk.Label(frame, text="Welcome to K Bank", font = "Georgia 25", pady = 10)
    instructions.pack()

    pin_label = tk.Label(frame, text = "Account Number", font = "Georgia", pady = 5)
    pin_label.pack()

    pin_entry = tk.Entry(frame, width = 30)
    pin_entry.pack()

    
    

    root.mainloop()
    '''



