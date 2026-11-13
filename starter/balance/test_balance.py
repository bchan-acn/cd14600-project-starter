import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TestBalance(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_initial_balance(self):
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_singleton_instance(self):
        balance1 = Balance.get_instance()
        balance2 = Balance.get_instance()
        self.assertIs(balance1, balance2)

    def test_direct_construction_preserves_shared_balance(self):
        self.balance.add_income(100)
        direct_balance = Balance()
        self.assertIs(direct_balance, self.balance)
        self.assertEqual(direct_balance.get_balance(), 100)

    def test_add_income(self):
        self.balance.add_income(100)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_add_expense(self):
        self.balance.add_expense(40)
        self.assertEqual(self.balance.get_balance(), -40)

    def test_apply_transaction_income(self):
        t = Transaction(150, TransactionCategory.INCOME)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 150)

    def test_apply_transaction_expense(self):
        t = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), -60)

    def test_apply_transaction_invalid_category(self):
        class FakeCategory:
            pass
        t = Transaction(100, FakeCategory())
        with self.assertRaises(ValueError):
            self.balance.apply_transaction(t)

    def test_reset(self):
        self.balance.add_income(100)
        self.balance.add_expense(50)
        self.balance.reset()
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_summary(self):
        self.balance.add_income(12.5)
        self.assertEqual(self.balance.summary(), "Net balance: 12.50")

    def test_observer_notified_with_balance_and_transaction(self):
        class Recorder:
            def __init__(self):
                self.calls = []

            def update(self, balance, transaction):
                self.calls.append((balance.get_balance(), transaction))

        recorder = Recorder()
        self.balance.register_observer(recorder)
        self.addCleanup(self.balance.unregister_observer, recorder)

        t = Transaction(80, TransactionCategory.INCOME)
        self.balance.apply_transaction(t)
        self.assertEqual(recorder.calls, [(80, t)])

    def test_duplicate_registration_notifies_once(self):
        class Counter:
            count = 0

            def update(self, balance, transaction):
                self.count += 1

        counter = Counter()
        self.balance.register_observer(counter)
        self.balance.register_observer(counter)
        self.addCleanup(self.balance.unregister_observer, counter)

        self.balance.apply_transaction(Transaction(1, TransactionCategory.INCOME))
        self.assertEqual(counter.count, 1)

    def test_unregistered_observer_not_notified(self):
        class Counter:
            count = 0

            def update(self, balance, transaction):
                self.count += 1

        counter = Counter()
        self.balance.register_observer(counter)
        self.balance.unregister_observer(counter)
        self.balance.unregister_observer(counter)  # no error when absent

        self.balance.apply_transaction(Transaction(1, TransactionCategory.INCOME))
        self.assertEqual(counter.count, 0)

    def test_invalid_transaction_does_not_notify(self):
        class Counter:
            count = 0

            def update(self, balance, transaction):
                self.count += 1

        class FakeCategory:
            pass

        counter = Counter()
        self.balance.register_observer(counter)
        self.addCleanup(self.balance.unregister_observer, counter)

        with self.assertRaises(ValueError):
            self.balance.apply_transaction(Transaction(5, FakeCategory()))
        self.assertEqual(counter.count, 0)

if __name__ == "__main__":
    unittest.main()
