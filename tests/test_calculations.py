import pytest
from tests.calculations import add, BankAccount

@pytest.fixture 
def zero_bank_account(): # Class test functions will call this function before they are run
    return BankAccount()

@pytest.fixture 
def bank_account():
    return BankAccount(50)

def test_add():
    print("testing add function")
    result = add(5, 3)
    assert add(5, 3) == 8

def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80