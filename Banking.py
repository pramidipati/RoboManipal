from abc import ABC, abstractmethod

class InsufficientFunds(Exception): pass
class InvalidAccount(Exception): pass
class FraudDetected(Exception): pass

class Account(ABC):
    def __init__(self, acc_no, owner, balance=0):
        self.acc_no, self.owner, self.balance = acc_no, owner, balance
        self.daily_total = 0
    @abstractmethod
    def account_type(self): pass
    def deposit(self, amount):
        if amount <= 0: raise ValueError
        self.balance += amount
        self.daily_total += amount
    def withdraw(self, amount):
        if amount > self.balance: raise InsufficientFunds
        if self.daily_total + amount > 10000: raise FraudDetected
        self.balance -= amount
        self.daily_total += amount

class SavingsAccount(Account):
    def account_type(self): return "Savings"

class CheckingAccount(Account):
    def account_type(self): return "Checking"

class BankOperations(ABC):
    @abstractmethod
    def transfer(self, from_acc, to_acc, amount): pass

class Bank(BankOperations):
    def __init__(self): self.accounts = {}
    def add_account(self, acc): self.accounts[acc.acc_no] = acc
    def get_account(self, acc_no):
        if acc_no not in self.accounts: raise InvalidAccount
        return self.accounts[acc_no]
    def transfer(self, from_acc_no, to_acc_no, amount):
        f = self.get_account(from_acc_no)
        t = self.get_account(to_acc_no)
        f.withdraw(amount)
        t.deposit(amount)

if __name__ == "__main__":
    bank = Bank()
    a1 = SavingsAccount("S1","Alice",5000)
    a2 = CheckingAccount("C1","Bob",2000)
    bank.add_account(a1)
    bank.add_account(a2)
    a1.deposit(2000)
    a1.withdraw(3000)
    bank.transfer("S1","C1",1500)
    try: a1.withdraw(9000)
    except FraudDetected: print("Fraud detected")
    print(a1.balance, a2.balance)
