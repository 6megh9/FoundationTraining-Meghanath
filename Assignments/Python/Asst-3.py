import mysql.connector as con
from mysql.connector import Error
connect = con.connect(host = "localhost",user = "root",password = "Root",database = "sakila")

# get account_balance
def get_balance():
    AccNo = input("Enter Account No: ")
    data =(AccNo,)
    sql = "select balance from accounts where Accno = %s;"
    c = connect.cursor()
    c.execute(sql,data)
    list1 = c.fetchone()
    print(f" The balance of the Account {AccNo} is:", list1[0])
    menu()
# deposit
def deposit_amount():
    AccNo = input("Enter Account No: ")
    Amount = int(input("Enter amount: "))
    data = (AccNo,)
    sql = "Select balance from accounts where AccNo = %s; "
    c = connect.cursor()
    c.execute(sql, data)
    list1 = c.fetchone()
    deposit = sum(list1, Amount)
    data1 = (deposit, AccNo)
    sql1 = " update Accounts set balance = %s where AccNo = %s;"
    c.execute(sql1,data1)
    print("Amount deposited...")
    print("The Current balance of the Account {Accno} is: ",deposit)
    menu()

#withdraw
def withdraw_amount():
    AccNo = input("Enter Account No: ")
    Amount = int(input("Enter amount: "))
    data = (AccNo,)
    sql = "Select balance from accounts where AccNo = %s; "
    c = connect.cursor()
    c.execute(sql, data)
    list1 = c.fetchone()
    if(Amount > list1[0]):
        print("Withdrawl not possible....\n Insufficient funds...")
        menu()
    else:
      withdraw = list1[0] - Amount
      data1 = (withdraw, AccNo)
      sql1 = " update Accounts set balance = %s where AccNo = %s;"
      c.execute(sql1, data1)
      print("Amount Withdrawl successful....")
      print("The Current balance of the Account {Accno} is: ", withdraw)
      menu()

#transfer
def transfer():
    pass
    '''Sender = input("Sender Account No: ")
    Receiver = input("Receiver Account No: ")
    Amount= input("Enter Amount: ")
    data = (Sender,)
    data1 = (Receiver,)
    query1 = "select balance from accounts where AccNo = %s; "
    c = connect.cursor()
    c.execute(query1, data1)
    receive = c.fetchall()
    deposit = receive + Amount
    print(list)'''
    menu()
#get transactions
def get_transactions():
    print("....View Transactions...")
    AccNo = input("Enter Acc No: ")
    data = (AccNo,)
    query = " select * from transactions where account = %s;"
    c = connect.cursor()
    c.execute(query, data)
    list = c.fetchall()
    for i in list:
        print("Account Number: ", i[0])
        print("Description: ", i[1])
        print("Date and Time: ", i[2])
        print("Transaction Type: ", i[3])
        print("Amount: ", i[4])
        print("-----------------------------")
        menu()

#create account
def create_account():
    AccNo = input("Enter Account No: ")
    if(check_account(AccNo) == True):
          print("Account already exists....")
          menu()
    else:
        AccType = input("Enter Account type: ")
        Balance = input("Enter Balance: ")
        CusName = input("Enter Customer Name: ")

        data = (AccNo, AccType, Balance, CusName)
        sql = " insert into accounts values (%s,%s,%s,%s);"
        c = connect.cursor()
        c.execute(sql, data)
        connect.commit()
        print(".......Account created successfully....")
        menu()

# check accountno
def check_account(AccNo):
    sql = 'select * from accounts where AccNo=%s'
    c = connect.cursor(buffered=True)
    data = (AccNo,)
    c.execute(sql, data)
    r = c.rowcount
    if r == 1:
        return True
    else:
        return False


#list accounts
def list_accounts():
    print("....View Accounts Details...")
    AccNo = input("Enter Acc No: ")
    data = (AccNo,)
    query = " select * from accounts where AccNo = %s;"
    c = connect.cursor()
    c.execute(query, data)
    list = c.fetchall()
    for i in list:
        print("Account Number: ", i[0])
        print("Account Type: ", i[1])
        print("Balance: ", i[2])
        print("Customer Name : ", i[3])
        print("-----------------------------")
        menu()


#get account details
def get_customer_details():
    print("....View Customer Details...")
    CusId = input("Enter Customer Id: ")
    data = (CusId,)
    query = " select * from customers where customerId = %s; "
    c = connect.cursor()
    c.execute(query, data)
    list = c.fetchall()
    for i in list:
      print("Customer Id: ", i[0])
      print("First_Name: ", i[1])
      print("Last_Name: ", i[2])
      print("Email : ", i[3])
      print("Phone Number : ", i[4])
      print("Address : ", i[5])
      print("-----------------------------")
      menu()


#calculate interest
def calculate_interest():
    Principal = int(input("Enter Principal Amount: "))
    Rate = int(input("Enter rate of interest : %"))
    Time = int(input("Enter years: "))
    Interest = Principal* Rate *Time
    print(f"The calculated Interest of Amount {Principal} is : ", Interest)
    menu()
#creating menu
def menu():
       print("Welcome to bank")
       print ("Select an option:")
       print("1.To create new account")
       print("2.Deposit amount")
       print("3.Withdraw amount")
       print("4.Get balance Amount")
       print("5.Get  Customer details")
       print("6.Transfer")
       print("7.List Accounts")
       print("8.Get Transactions ")
       print("9.Calculate interest ")
       print("10.Exit")

       option = input("Enter option: ")

       if option == '1':
           create_account()
       elif option == '2':
           deposit_amount()
       elif option== '3':
           withdraw_amount()
       elif option == '4':
           get_balance()
       elif option == '5':
         get_customer_details()
       elif option == '6':
          transfer()
       elif option == '7':
          list_accounts()
       elif option == '8':
          get_transactions()
       elif option == '9':
          calculate_interest()
       elif option == '10':
           print("....Exit....")

       else:
          print("Invalid option...\n Try again...")
          menu()

menu()