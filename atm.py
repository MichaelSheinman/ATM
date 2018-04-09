
# By: Michael Sheinman
# Date: 2018-03-28 13:31:37.934330
# File Name: ATM project
# Description: Making a bank project
import sys
import os
import time
import re
from datetime import datetime
from decimal import Decimal

#Niko added some chainges here

# Function to change the user file. Complete
def replaceFile(account, file):
   os.remove(account + '.txt')
   userFile = open(account + '.txt', 'w')
   # Rewrite here
   for line in range(len(file)):
       userFile.write(str(file[line]) + '\n')
   userFile.close()
   return file


# Recursion to make sure the pin numbers are the same
def equal(p):
   # If there is only one number left, we know all were equal
   if len(p) == 1:
       return True
   else:
       if p[0] == p[1]:
           # If they are equal, we have to check the next ones
           return equal(p[1:])
       else:
           return False

# Handles special cases such as 20 & 8 transactions
def is_special(account, file):
   myFile = open(account + 'history.txt')
   allTransactions = myFile.readlines()
   if len(allTransactions) % 8 == 0:
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s" % (
       now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-4.00) + '\n')
       if Decimal(file[4]) >= 4:
           balance = file[4]
           file.pop(4)
           file.insert(4, str(Decimal(balance) - Decimal(4)))  # at place 4 I insert the money - 4
       elif 0 < Decimal(file[4]) < 4:
           difference = 4 - Decimal(file[4])
           file.pop(4)
           file.pop(4)
           file.insert(4, str(0))
           file.insert(5, str(Decimal(file[5]) -difference))
           file = overdraftfunction(difference, file[2], current_time, file)
       else:
           to_be_used = file[5]
           file.pop(5)
           file.insert(5, Decimal(to_be_used) - 4)
   elif len(allTransactions) % 40 == 0:
       history_file = open(account + 'history.txt', 'r')
       myhistory = history_file.readlines()
       total = 0
       print("You have reached 20 transactions. Here they are:")
       for a in range(len(myhistory)):
           if not a % 2 == 0:
               total += Decimal(myhistory[a].split('\n')[0])
           sys.stdout.write(myhistory[a])
       if total > 0:
           print("\nYour net income is: %s" % total)
       else:
           print("\nYour net lose is: %s" % total)

   pass

# Account details.
def view(file):
   print(file)
   print("Account details:")
   print("_______________________")
   print("Card number: %s" % file[0])
   print("Balance: %s" % file[4])
   print("Overdraft: %s" % file[5])
   time.sleep(2)


# Printing transaction history
def print_transaction(account):
   transactions = open(account + 'history.txt', 'r')
   allTransactions = transactions.readlines()
   transactions.close()
   if len(allTransactions) == 0:
       print("No transactions yet")
   else:
       print("Transactions:")
       for tran in range(len(allTransactions)):
           sys.stdout.write(allTransactions[tran])


# Replacing the pin
def pin(current, account, file):
   while True:
       pin = input("Enter the new pin(must be 4 digits): ")
       if not re.search(r'^\d{4}$', pin):
           continue
       if equal(pin):
           continue
       if pin == current:
           continue
       if pins_check(pin):
           break
       else:
           print("This pin already exists")
   file.pop(1)
   file.insert(1, str(pin))
   sys.stdout.write("Changing pin")
   name = "....\n"
   for char in name:
       sys.stdout.write(char)
       sys.stdout.flush()
       time.sleep(.5)
   return replaceFile(account, file)


def withdraw(money, overdraft, file, account, gone_overdraft):
   if overdraft == 'True':
       gone_overdraft = Decimal(gone_overdraft)
   allOptions = {'1': 20, '2': 40, '3': 60, '4': 80, '5': 100, '6': 120, '7': 'other'}
   while True:
       option = input("Pick a withdraw option: 1) $20 2) $40 3) $60 4) $80 5) $100 6) $120 7) Other: ")
       if option not in allOptions.keys():
           continue
       break
   withdrawen = allOptions[option]
   if withdrawen == 'other':
       while True:
           withdrawen = input("Enter an amount: ")
           try:
               if Decimal(withdrawen) > 0:
                   break
           except Exception:
               continue
   withdrawen = Decimal(withdrawen)
   if money > withdrawen or overdraft == 'True' and money + gone_overdraft > withdrawen:
       sys.stdout.write("dispensing money")
       name = ".....\n"
       for char in name:
           sys.stdout.write(char)
           sys.stdout.flush()
           time.sleep(.5)
       if money > withdrawen:
           file.pop(4)
           file.insert(4, str(money - withdrawen))
       else:
           difference = withdrawen - money
           gone_overdraft -= difference
           now = datetime.now()
           current_time = "%s:%s %s / %s / %s" % (
           now.hour, now.minute, now.month, now.day, now.year)
           file =  overdraftfunction(gone_overdraft, file[2], current_time, file)
           money = 0
           file.pop(4)
           file.pop(4)
           file.insert(4, money)
           file.insert(5, gone_overdraft)

       # Rewrite file point
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s" % (now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-withdrawen) + '\n')
       history_file.close()
       is_special(account, file)
       return replaceFile(account, file)
   else:
       print("No enough money")
       return file


def deposit(file, userMoney, account):
   allDeposits = []
   while True:
       while True:
           money = input("Enter money to Deposit(done to quit): ".lower())
           try:
               if Decimal(money) < 0:
                   continue
               break
           except Exception:
               # Value error means a string was entered
               if money == "done":
                   break
               else:
                   continue

       if money != 'done':
           allDeposits.append(money)
           time.sleep(2)
           print("Deposit accepted")
       else:
           break
   total = 0
   for i in range(len(allDeposits)):
       total += Decimal(allDeposits[i])
   if file[3] == 'True' and Decimal(file[5]) < 500:
       if total + Decimal(file[5]) <= 500:
           newOverDraft = Decimal(file[5]) + total
       else:
           subtract = total - Decimal(file[5])
           newOverDraft = 500
           another_varaible_to_store_total = total - subtract
           userMoney += another_varaible_to_store_total
   else:
       userMoney += total
       if file[3] == 'True':
           newOverDraft = 500
       else:
           newOverDraft = "Not in action"
   file.pop(4)
   file.insert(4, str(userMoney))
   file.pop(5)
   file.insert(5, str(newOverDraft))
   now = datetime.now()
   current_time = "%s:%s %s / %s / %s\n" % (now.hour, now.minute, now.month, now.day, now.year)
   history_file = open(account + 'history.txt', 'a')
   history_file.write(current_time)
   history_file.write(str(total) + '\n')
   history_file.close()
   is_special(account, file)
   return replaceFile(account, file)


# Function that will notify the user when they go beyond overdraft
def overdraftfunction(howfar, email, time, file):
   import smtplib
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText

   # variables for to and from
   the_overdraft = str(Decimal(file[5]) - Decimal(howfar))
   charge = str(Decimal(the_overdraft) * Decimal(0.25))
   howfar -= Decimal(charge)
   myadd = "casinogames99@gmail.com"
   youradd = email

   msg = MIMEMultipart()
   msg['From'] = myadd
   msg['To'] = youradd
   msg['Subject'] = "ATM project"

   # body of text
   body = "Dir Sir/Madam, Your recent transaction at (%s) shows that you have gone into your overdraft.  " \
          "You overdraft protection is $%s.  " \
          "You have gone $%s into your overdraft, leaving you with a balance of $%s in your overdraft. " \
          "This is including a small service charge of $%s (25 percent of $%s) has been added to your account. Thank you." % \
          (time, file[5], the_overdraft, howfar, charge, the_overdraft)
   msg.attach(MIMEText(body, "plain"))

   server = smtplib.SMTP("smtp.gmail.com", 587)
   server.starttls()
   server.login(myadd, 'mikejack')
   text = msg.as_string()
   server.sendmail(myadd, youradd, text)
   server.quit()
   to_be_used = file[5]
   file.pop(5)
   file.insert(5, str(Decimal(to_be_used) - Decimal(charge)))
   return replaceFile(file[0], file)


# Function that lets the user pay bills
def bills(file, userMoney, account, overdraft, email, overdraftAmount):
   if overdraft == 'True':
       overdraftAmount = Decimal(overdraftAmount)
   billName = input("Enter bill name: ")
   while True:
       accountNumber = input("Enter account number(must be 6 digits): ")
       if re.search(r'^\d{6}$', accountNumber):
           break
   while True:
       amount = input("Enter amount to be paid: ")
       try:
           if Decimal(amount) > 0:
               break
           else:
               continue
       except Exception:
           # Exception indicates decimal error.
           continue
   amount = Decimal(amount)
   # The if statements checks where the money should go (overdraft/balance)
   if userMoney > amount or overdraft == 'True' and userMoney + overdraftAmount > amount:
       if userMoney > amount:
           userMoney -= amount
           file.pop(4)
           file.insert(4, userMoney)
       else:
           userMoney = 0
           goneIntoOverdraft = overdraftAmount - (amount - userMoney)
           now = datetime.now()
           current_time = "%s:%s %s / %s / %s" % (
           now.hour, now.minute, now.month, now.day, now.year)
           file = overdraftfunction(goneIntoOverdraft, email, current_time, file)
           file.pop(4)
           file.pop(4)
           file.insert(4, userMoney)
           file.insert(5, goneIntoOverdraft)
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s\n" % (now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-amount) + '\n')
       history_file.close()
       is_special(account, file)
       return replaceFile(account, file)
   else:
       print("Not enough money")
       return file


def menu(file):
   while True:
       print("Welcome to the menu. You may pick one of the following options:"
             "\n1. View your account details"
             "\n2. Change PIN"
             "\n3. Withdraw money"
             "\n4. Deposit money"
             "\n5. Pay bills"
             "\n6. View History"
             "\n7. Quit")
       navigation = input("Pick option: ")
       if navigation == '1':
           view(file)
       elif navigation == '2':
           file = pin(file[1], file[0], file)
       elif navigation == '3':
           file = withdraw(Decimal(file[4]), file[3], file, file[0], file[5])
       elif navigation == '4':
           file = deposit(file, Decimal(file[4]), file[0])
       elif navigation == '5':
           file = bills(file, Decimal(file[4]), file[0], file[3], file[2], file[5])
       elif navigation == '6':
           print_transaction(file[0])
       elif navigation == '7':
           print_transaction(file[0])
           return


def pins_check(pin_input):
   if os.path.exists('pins.txt'):
       pins = open('pins.txt', 'r')
       myFile = pins.readlines()
       pins.close()
       for pin in range(len(myFile)):
           new = myFile[pin].replace('\n', '')
           myFile.pop(pin)
           myFile.insert(pin, new)
       if pin_input in myFile:
           return False
       else:
           myPin = open('pins.txt', 'a')
           myPin.write(pin_input + '\n')
           myPin.close()
           return True

   else:
       pins = open('pins.txt', 'w')
       pins.write(pin_input + '\n')
       pins.close()
       return True

def signup():
   # Card input
   while True:
       card = input("Enter the card number(must be 4 digits): ")
       if not re.search(r'^\d{4}$', card):
           continue
       if equal(card):
           continue
       break
   # PIN input
   while True:
       pin = input("Enter the pin number(must be 4 digits): ")
       if not re.search(r'^\d{4}$', pin):
           continue
       if equal(pin):
           continue
       if pins_check(pin):
           break
       else:
           print("The pin already exists")
   # Gmail input
   while True:
       email = input("Enter email(gmail only): ")
       if '@gmail.com' in email:
           break
   # Overdraft protection input
   while True:
       print("Would you like to sign up for overdraft protection?")
       prompt_overdraft = input("y for yes, n for no, i for 'what is overdraft?' ")
       if prompt_overdraft == 'y' or prompt_overdraft == 'yes':
           overdraft = 'True'
           break
       elif prompt_overdraft == 'n' or prompt_overdraft == 'no':
           overdraft = 'False'
           break
       elif prompt_overdraft == 'i':
           print("Overdraft allows you to go beyond 0 to maximum of $500\n"
                 "Each time you go beyond the overdraft, you will be charged with 25% of your overdraft\n"
                 "An email will be sent to you each time you go beyond the overdraft. ")
   userFile = open(card + '.txt', 'w')
   userFile.write(card + '\n' + pin + '\n' + email + '\n' + overdraft + '\n' + '0' + '\n')
   if overdraft == 'True':
       userFile.write('500')
   else:
       userFile.write('Not in action')
   userFile.close()
   user_history_file = open(card + 'history.txt', 'w')
   user_history_file.close()
   sys.stdout.write("redirecting to login")
   name = ".....\n"
   for char in name:
       sys.stdout.write(char)
       sys.stdout.flush()
       time.sleep(.6)
   login()


def login():
   while True:
       card_login = input("Enter your card number: ")
       if not os.path.exists(card_login + '.txt'):
           continue
       break
   user_file = open(card_login + '.txt')
   userLines = user_file.readlines()
   # The process of removing the line spacing
   for line in range(len(userLines)):
       new = userLines[line].replace('\n', '')
       userLines.pop(line)
       userLines.insert(line, new)
   user_file.close()

   actual_pin = userLines[1]
   while True:
       pin_login = input("Enter your pin: ")
       if not pin_login == actual_pin:
           continue
       break

   menu(userLines)
   return


while True:
   enter = input("Would you like to sign in(I) or sign up(U): ".lower())
   if enter == 'i':
       login()
       break
   elif enter == 'u':
       signup()
       break


