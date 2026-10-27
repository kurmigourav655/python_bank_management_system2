import json
import os


class BankAccount:

    def __init__(self, account_no, name, pin, balance=0):
        self.account_no = account_no
        self.name = name
        self.pin = pin
        self.balance = balance
        self.transactions = []

    # Deposit
    def deposit(self, amount):

        if amount > 0:
            self.balance += amount

            self.transactions.append(
                f"Deposited: ₹{amount}"
            )

            print("Amount deposited successfully.")

            save_data()

        else:
            print("Invalid amount.")

    # Withdraw
    def withdraw(self, amount):

        if amount <= 0:
            print("Invalid amount.")

        elif amount > self.balance:
            print("Insufficient balance.")

        else:
            self.balance -= amount

            self.transactions.append(
                f"Withdrawn: ₹{amount}"
            )

            print("Amount withdrawn successfully.")

            save_data()

    # Check Balance
    def check_balance(self):

        print("Current Balance: ₹", self.balance)

    # Account Details
    def account_details(self):

        print("\n----- ACCOUNT DETAILS -----")

        print("Account Number:", self.account_no)
        print("Name:", self.name)
        print("Balance: ₹", self.balance)

    # Change PIN
    def change_pin(self, old_pin, new_pin):

        if self.pin == old_pin:

            if len(str(new_pin)) == 4:

                self.pin = new_pin

                print("PIN changed successfully.")

                save_data()

            else:
                print("PIN must be exactly 4 digits.")

        else:
            print("Wrong old PIN.")

    # Transaction History
    def transaction_history(self):

        print("\n----- TRANSACTION HISTORY -----")

        if len(self.transactions) == 0:

            print("No transactions found.")

        else:

            for transaction in self.transactions:

                print(transaction)

    # Transfer Money
    def transfer(self, receiver_account, amount):

        if amount <= 0:

            print("Invalid amount.")

        elif amount > self.balance:

            print("Insufficient balance.")

        else:

            self.balance -= amount

            receiver_account.balance += amount

            # Sender transaction
            self.transactions.append(
                f"Transferred: ₹{amount} to Account "
                f"{receiver_account.account_no}"
            )

            # Receiver transaction
            receiver_account.transactions.append(
                f"Received: ₹{amount} from Account "
                f"{self.account_no}"
            )

            print("Money transferred successfully.")

            save_data()


# ==========================================
# ALL ACCOUNTS
# ==========================================

accounts = {}


# Starting Account Number
next_account_no = 1001


# ==========================================
# SAVE DATA
# ==========================================

def save_data():

    data = {}

    for account_no, account in accounts.items():

        data[account_no] = {

            "name": account.name,

            "pin": account.pin,

            "balance": account.balance,

            "transactions": account.transactions
        }

    with open("data.json", "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    global accounts
    global next_account_no

    if os.path.exists("data.json"):

        with open("data.json", "r") as file:

            data = json.load(file)

        for account_no, details in data.items():

            account = BankAccount(

                int(account_no),

                details["name"],

                details["pin"],

                details["balance"]
            )

            account.transactions = details["transactions"]

            accounts[int(account_no)] = account

        if len(accounts) > 0:

            next_account_no = max(accounts.keys()) + 1


# ==========================================
# CREATE ACCOUNT
# ==========================================

def create_account():

    global next_account_no

    print("\n----- CREATE ACCOUNT -----")

    name = input("Enter your name: ")

    # PIN Validation
    while True:

        try:

            pin = int(
                input("Create 4-digit PIN: ")
            )

            if 1000 <= pin <= 9999:

                break

            else:

                print("PIN must be exactly 4 digits.")

        except ValueError:

            print("Please enter numbers only.")

    # Initial Balance
    while True:

        try:

            initial_balance = float(
                input("Enter initial deposit: ")
            )

            if initial_balance >= 0:

                break

            else:

                print("Balance cannot be negative.")

        except ValueError:

            print("Please enter a valid amount.")

    # Create Account
    account = BankAccount(

        next_account_no,

        name,

        pin,

        initial_balance
    )

    accounts[next_account_no] = account

    # Initial transaction
    if initial_balance > 0:

        account.transactions.append(
            f"Initial Deposit: ₹{initial_balance}"
        )

    save_data()

    print("\nAccount created successfully!")

    print(
        "Your Account Number is:",
        next_account_no
    )

    next_account_no += 1


# ==========================================
# LOGIN
# ==========================================

def login():

    try:

        account_no = int(
            input("Enter Account Number: ")
        )

        pin = int(
            input("Enter PIN: ")
        )

    except ValueError:

        print("Please enter valid numbers.")

        return

    if account_no in accounts:

        account = accounts[account_no]

        if account.pin == pin:

            print("\nLogin successful!")

            print(
                f"Welcome, {account.name}"
            )

            account_menu(account)

        else:

            print("Wrong PIN.")

    else:

        print("Account not found.")


# ==========================================
# TRANSFER MONEY
# ==========================================

def transfer_money(account):

    try:

        receiver_no = int(
            input(
                "Enter Receiver Account Number: "
            )
        )

    except ValueError:

        print("Invalid account number.")

        return

    # Check Receiver
    if receiver_no not in accounts:

        print("Receiver account not found.")

        return

    # Prevent self transfer
    if receiver_no == account.account_no:

        print(
            "You cannot transfer money to your own account."
        )

        return

    try:

        amount = float(
            input(
                "Enter amount to transfer: "
            )
        )

    except ValueError:

        print("Invalid amount.")

        return

    receiver_account = accounts[receiver_no]

    account.transfer(
        receiver_account,
        amount
    )


# ==========================================
# ACCOUNT MENU
# ==========================================

def account_menu(account):

    while True:

        print("\n================================")
        print("          ACCOUNT MENU")
        print("================================")

        print("1. Account Details")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Change PIN")
        print("6. Transaction History")
        print("7. Transfer Money")
        print("8. Logout")

        choice = input(
            "Enter your choice: "
        )

        # Account Details
        if choice == "1":

            account.account_details()

        # Deposit
        elif choice == "2":

            try:

                amount = float(
                    input(
                        "Enter amount to deposit: "
                    )
                )

                account.deposit(amount)

            except ValueError:

                print("Invalid amount.")

        # Withdraw
        elif choice == "3":

            try:

                amount = float(
                    input(
                        "Enter amount to withdraw: "
                    )
                )

                account.withdraw(amount)

            except ValueError:

                print("Invalid amount.")

        # Check Balance
        elif choice == "4":

            account.check_balance()

        # Change PIN
        elif choice == "5":

            try:

                old_pin = int(
                    input(
                        "Enter old PIN: "
                    )
                )

                new_pin = int(
                    input(
                        "Enter new PIN: "
                    )
                )

                account.change_pin(
                    old_pin,
                    new_pin
                )

            except ValueError:

                print("PIN must contain numbers only.")

        # Transaction History
        elif choice == "6":

            account.transaction_history()

        # Transfer Money
        elif choice == "7":

            transfer_money(account)

        # Logout
        elif choice == "8":

            print(
                "Logged out successfully."
            )

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


# ==========================================
# LOAD OLD DATA
# ==========================================

load_data()


# ==========================================
# MAIN PROGRAM
# ==========================================

while True:

    print("\n================================")
    print("      BANK MANAGEMENT SYSTEM")
    print("================================")

    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input(
        "Enter your choice: "
    )

    # Create Account
    if choice == "1":

        create_account()

    # Login
    elif choice == "2":

        login()

    # Exit
    elif choice == "3":

        save_data()

        print(
            "\nThank you for using "
            "Bank Management System."
        )

        break

    else:

        print(
            "Invalid choice. Please try again."
        )