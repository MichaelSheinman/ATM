# By: Michael Sheinman
# Date: Wenseday, Febuary 27
# File: Business Application
# Business Application for Bucks Bank




def deposit(file, account, amount=False):
    if not amount:
        while True:
            try:
                amount = int(input("Enter amount to deposit: "))
                break
            except ValueError:
                print("Only enter integers")

    add_history(account, 'Deposit', file[account][0], amount)
    file[account][0] += amount

    if file[account][1] == 'Basic':
        add_everyday_free(file, account)
    elif file[account][1] == 'Unlimited':
        add_unlimited_transactions(file, account)


def withdraw(file, account, amount=False):
    if not amount:
        while True:
            try:
                amount = int(input("Enter amount to withdraw: "))
                break
            except ValueError:
                print("Only enter integers")
    if amount < file[account][0]:
        file[account][0] -= amount
        add_history(account, 'Withdraw', file[account][0], -amount)

        if file[account][1] == 'Unlimited':
            add_unlimited_transactions(file, account)
        elif file[account][1] == "Basic":
            add_everyday_free(file, account)
    else:
        print("You do not have enough money")



def add_history(account, type, balance, amount):
    global current_history
    """A helper method to add to the history"""
    if account in current_history.keys():
        current_history[account].append([type, balance, amount])
    else:
        current_history[account] = [[type, balance, amount]]



def add_everyday_free(file, account):
    previous_balance = file[account][0]
    transaction_fee = 1
    file[account][0] -= transaction_fee
    add_history(account, 'Everyday plan fee', previous_balance, -transaction_fee)


def add_unlimited_transactions(file, account):
    if file[account][2] > 25:
        previous_balance = file[account][0]
        transaction_fee = 0.5
        file[account][0] -= transaction_fee
        add_history(account, 'Unlimited plan fee', previous_balance, -transaction_fee)
    else:
        file[account][2] += 1

def bills(file, account):
    """A function used to pay bills"""
    while True:
        sub_menus = input("Choose between the following three plans:\n"
                          "1. Add Payee: Company Name, Company's account number\n"
                          "2. Pay Bill: Choose from a list of payees\n"
                          "3. Automatic Bill Payment, choose a payee and process payment monthly\nEnter Choice: ")
        try:
            sub_menus = int(sub_menus)
            break
        except Exception:
            print("Choose an integer only(1, 2, 3)")

    if sub_menus == 1:
        company_name = input("Enter company name: ")
        amount = int(input("Enter amount to pay: "))
        file[company_name] = [amount, 'Basic']
        add_history(account, 'Bill Paid', file[account][0], -amount)
        add_history(company_name, 'Bill Received', amount, amount)

        # This will be changed in future, but for now all plans are baisc
        add_everyday_free(file, account)


    elif sub_menus == 2:
        all_people = file.keys()

        print("Choose a person to transform money to, from the following list")
        for ii, x in enumerate(all_people):
            print("Person %s: %s" % (ii+1, x))

        my_person = input("Choose the person: ")
        amount = int(input("Choose the amount: "))
        previous_balance = file[my_person][0]
        file[my_person][0] += amount
        add_history(account, 'Bill Paid', file[account][0], -amount)
        add_history(my_person, 'Bill Recieved', previous_balance, amount)
        add_everyday_free(file, account)

    elif sub_menus == 3:
        all_people = file.keys()
        for ii, x in enumerate(all_people):
            print("Person %s: %s" % (ii+1, x))
        payee = input("Enter the person the monthly payment is delivered to: ")
        amount = int(input("Enter an amount: "))
        # TODO: Add Deposit/Withdraw
        if 'D' not in monthly_transactions:
            monthly_transactions['D'] = [[payee, amount]]
        else:
            monthly_transactions['D'].append([payee, amount])
        if 'W' not in monthly_transactions:
            monthly_transactions['W'] = [[account, amount]]
        else:
            monthly_transactions['W'].append([account, amount])


def view(file, account):
    print(file)
    print("Account details:")
    print("_______________________")
    print("Balance: %s" % file[account][0])
    print(file[account])
    print("Plan: %s" % file[account][1])


def print_history(history):
    """This function prints the current history"""
    for acc in current_history:
        print("Account: %s" % acc)
        print("-----------------------------------------------------------------------")
        transactions = history[acc]
        print("Transactions: ")
        for counter, each in enumerate(transactions):
            print("Transaction #%s: Type: %s, Balance: %s, Change: %s" % (counter+1, each[0], each[1], each[2]))



def monthly_payments(file, payments):
    for each in payments:
        if each == 'D':
            deposit(file, payments[each])
        elif each == 'W':
            withdraw(file, payments[each])


def change_service_plan(file, account):
    print("Our service plans include"
          "\n1. All-Inclusive: Maximum overdraft $500, fee is $25 per month, ulimited transactions"
          "\n2. Unlimited: Maximum overdraft $250, fee is $12.5 per month, $250 dollar limit"
          "\n3. Everyday:  No overdraft, $1, per transaction.")

    new_plan = int(input("Enter new plan: "))
    if new_plan == 1:
        file[account][1] = 'Inclusive'
        if len(file[account]) > 2:
            file[account].pop(2)
    elif new_plan == 2:
        file[account][1] = 'Unlimited'
        file[account].append(0)   # This stands for the number of transactions, since we have 25 free transactions
    elif new_plan == 3:
        file[account][1] = 'Basic'

def menu(file, account_numb):
    print("Current account: #%s" % account_numb)
    while True:
        print("Welcome to the menu. You may pick one of the following options:"
              "\n1. Choose an Account"
              "\n2. View your Current Balance"
              "\n3. Withdraw money"
              "\n4. Deposit money"
              "\n5. Pay bills"
              "\n6. View Monthly Transactions"
              "\n7. Change Service Plan"
              "\n8. Advance one month")
        navigation = input("Pick option: ")
        if navigation == '1':
            return
        if navigation == '2':
            view(file, account_numb)
        elif navigation == '3':
            withdraw(file, account_numb)
        elif navigation == '4':
            deposit(file, account_numb)
        elif navigation == '5':
            bills(file, account_numb)
        elif navigation == '6':
            print_history(current_history)
        elif navigation == '7':
            change_service_plan(file)
        elif navigation == '8':
            advance_one_month(file)


def advance_one_month(file):
    pay_interest(file)

    # TODO: Perform monthly payments
    all_deposit = monthly_transactions['D']
    all_withdraws = monthly_transactions['W']

    for depo in all_deposit:
        person = depo[0]
        amount = depo[1]
        deposit(file, person, amount)

    for wit in all_withdraws:
        person = wit[0]
        amount = wit[1]
        withdraw(file, person, amount)


def pay_interest(file):
    for customer in file.keys():
        balance = file[customer][0]
        if balance < 5000:
            interest = balance * 0
        elif 5000 <= balance and balance < 10000:
            interest = balance * 0.001
            file[customer][0] += interest
            add_history(customer, 'Interest', balance, interest)
        elif 10000 <= balance and balance < 25000:
            interest = balance * 0.002
            file[customer][0] += interest
            add_history(customer, 'Interest', balance, interest)
        elif 25000 <= balance and balance < 60000:
            interest = balance * 0.003
            file[customer][0] += interest
            add_history(customer, 'Interest', balance, interest)
        elif 60000 <= balance and balance < 5000000:
            interest = balance * 0.004
            file[customer][0] += interest
            add_history(customer, 'Interest', balance, interest)
        elif 5000000 >= balance:
            interest = balance * 0.005
            file[customer][0] += interest
            add_history(customer, 'Interest', balance, interest)




def choose_account():
    while True:
        account_numb = input("Enter your account number(-1 to quit): ")
        if account_numb == -1:
            break
        elif account_numb in my_accounts.keys():
            view(my_accounts, account_numb)
            menu(my_accounts, account_numb)
        else:
            print("This is an invalid account, please try again")


# Step 1: Read from the textfile
my_file = open('bucks_bank.txt', 'r')

letters = my_file.readlines()
my_accounts = {}
for x in letters:
    x = x.split(', ')
    new = x
    new[1] = new[1].replace('\n', '')
    my_accounts[new[0]] = [int(new[1]), 'Basic']

# To debug, database
# print(my_accounts)

monthly_transactions = {}

current_history = {}

# Starting the program, the user chooses an account
choose_account()