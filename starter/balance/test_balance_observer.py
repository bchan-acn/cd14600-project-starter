import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
import io
from contextlib import redirect_stdout
from balance.balance_observer import (
    IBalanceObserver,
    LowBalanceAlertObserver,
    PrintObserver,
)

class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.addCleanup(self.balance.reset)

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)
        
        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_no_alert_at_exact_threshold(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        self.balance.apply_transaction(Transaction(50, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

    def test_alert_message_printed_when_triggered(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        out = io.StringIO()
        with redirect_stdout(out):
            self.balance.apply_transaction(Transaction(10, TransactionCategory.INCOME))
        self.assertIn("ALERT", out.getvalue())

    def test_no_alert_message_when_balance_ok(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        out = io.StringIO()
        with redirect_stdout(out):
            self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertEqual(out.getvalue(), "")

    def test_base_observer_update_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            IBalanceObserver().update(self.balance, None)


class TestPrintObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.addCleanup(self.balance.reset)

    def test_prints_transaction_and_balance(self):
        observer = PrintObserver()
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        out = io.StringIO()
        with redirect_stdout(out):
            self.balance.apply_transaction(Transaction(25, TransactionCategory.INCOME))
        self.assertIn("Transaction($25", out.getvalue())
        self.assertIn("Net balance: 25.00", out.getvalue())

if __name__ == "__main__":
    unittest.main()
