import uuid

class User:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = str(uuid.uuid4())
        self.balance = 0
        self.transaction_history = []
        self.loans_taken = 0

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited {amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew {amount}")

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount, bank):
        if self.loans_taken >= 2:
            print("Loan limit exceeded")
        elif not bank.loan_feature_enabled:
            print("Loan feature is disabled")
        else:
            self.balance += amount
            self.loans_taken += 1
            self.transaction_history.append(f"Loan taken {amount}")

    def transfer(self, amount, recipient_account_number, bank):
        if self.balance < amount:
            print("Insufficient balance")
        else:
            recipient = bank.get_user_by_account_number(recipient_account_number)
            if recipient:
                self.balance -= amount
                recipient.balance += amount
                self.transaction_history.append(f"Transferred {amount} to {recipient_account_number}")
                recipient.transaction_history.append(f"Received {amount} from {self.account_number}")
            else:
                print("Account does not exist")

class Admin:
    def __init__(self, name, email, address, bank):
        self.name = name
        self.email = email
        self.address = address
        self.bank = bank

    def delete_account(self, account_number):
        user = self.bank.get_user_by_account_number(account_number)
        if user:
            self.bank.users.remove(user)
            print(f"Account {account_number} deleted")
        else:
            print("Account not found")

    def view_all_accounts(self):
        return [user.account_number for user in self.bank.users]

    def check_total_balance(self):
        return sum(user.balance for user in self.bank.users)

    def check_total_loan_amount(self):
        return sum(user.balance for user in self.bank.users if user.loans_taken > 0)

    def loan_feature(self):
        self.bank.loan_feature_enabled = not self.bank.loan_feature_enabled
        status = "enabled" if self.bank.loan_feature_enabled else "disabled"
        print(f"Loan feature is now {status}")

class Bank:
    def __init__(self):
        self.users = []
        self.loan_feature_enabled = True

    def get_user_by_account_number(self, account_number):
        for user in self.users:
            if user.account_number == account_number:
                return user
        return None

    def add_user(self, user):
        self.users.append(user)

def replica():
    bank = Bank()

    admin_name = input("Enter admin name: ")
    admin_email = input("Enter admin email: ")
    admin_address = input("Enter admin address: ")
    admin = Admin(admin_name, admin_email, admin_address, bank)

    while True:
        print("\nWelcome To The Bank:")
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            while True:
                print("\nAdmin Menu:")
                print("1. Delete Account")
                print("2. View All Accounts")
                print("3. Check Total Balance")
                print("4. Check Total Loan Amount")
                print("5. Loan Feature")
                print("6. Exit")
                c = int(input("Enter your choice: "))

                if c == 1:
                    account_number = input("Enter account number: ")
                    admin.delete_account(account_number)
                elif c == 2:
                    accounts = admin.view_all_accounts()
                    print("Accounts:", accounts)
                elif c == 3:
                    total_balance = admin.check_total_balance()
                    print("Total balance:", total_balance)
                elif c == 4:
                    total_loan_amount = admin.check_total_loan_amount()
                    print("Total loan amount:", total_loan_amount)
                elif c == 5:
                    admin.loan_feature()
                elif c == 6:
                    print("Exiting Admin Menu!")
                    break

        elif choice == 2:
            while True:
                print("\nUser Menu:")
                print("1. Create Account")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Check Balance")
                print("5. Check Transaction History")
                print("6. Take Loan")
                print("7. Balance Transfer")
                print("8. Exit")
                k = int(input("Enter your choice: "))

                if k == 1:
                    name = input("Enter your name: ")
                    email = input("Enter your email: ")
                    address = input("Enter your address: ")
                    account_type = input("Enter your account type: ")
                    user = User(name, email, address, account_type)
                    bank.add_user(user)
                    print(f"Account number: {user.account_number}")
                elif k == 2:
                    account_number = input("Enter your account number: ")
                    amount = int(input("Enter amount: "))
                    user = bank.get_user_by_account_number(account_number)
                    if user:
                        user.deposit(amount)
                        print(f"Deposited {amount}. New balance: {user.check_balance()}")
                    else:
                        print("Account not found")
                elif k == 3:
                    account_number = input("Enter your account number: ")
                    amount = int(input("Enter amount: "))
                    user = bank.get_user_by_account_number(account_number)
                    if user:
                        user.withdraw(amount)
                        print(f"Withdrew {amount}. New balance: {user.check_balance()}")
                    else:
                        print("Account not found")
                elif k == 4:
                    account_number = input("Enter your account number: ")
                    user = bank.get_user_by_account_number(account_number)
                    if user:
                        print("Balance:", user.check_balance())
                    else:
                        print("Account not found")
                elif k == 5:
                    account_number = input("Enter your account number: ")
                    user = bank.get_user_by_account_number(account_number)
                    if user:
                        print("Transaction History:", user.check_transaction_history())
                    else:
                        print("Account not found")
                elif k == 6:
                    account_number = input("Enter your account number: ")
                    amount = int(input("Enter amount: "))
                    user = bank.get_user_by_account_number(account_number)
                    if user:
                        user.take_loan(amount, bank)
                        print(f"Loan of {amount} taken. New balance: {user.check_balance()}")
                    else:
                        print("Account not found")
                elif k == 7:
                    account_number = input("Enter your account number: ")
                    recipient_account_number = input("Enter recipient account number: ")
                    amount = int(input("Enter amount: "))
                    user = bank.get_user_by_account_number(account_number)
                    if user:
                        user.transfer(amount, recipient_account_number, bank)
                        print(f"Transferred {amount} to {recipient_account_number}. New balance: {user.check_balance()}")
                    else:
                        print("Account not found")
                elif k == 8:
                    print("Exiting User Menu!")
                    break

        elif choice == 3:
            print("Exiting the Bank System!")
            break

replica()

