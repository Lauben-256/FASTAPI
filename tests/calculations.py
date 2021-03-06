def add(num1: int, num2: 2):
    return num1 + num2


class BankAccount():
    def __init__(self, starting_balancing=0):
        self.balance = starting_balancing 

    def deposit(self, amount):
        self.balance += amount 

    def withdraw(self, amount):
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1