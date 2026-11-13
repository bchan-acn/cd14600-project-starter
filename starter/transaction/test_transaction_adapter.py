import unittest
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TestTransactionAdapter(unittest.TestCase):

    def test_adapter_converts_freelance_income(self):
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()
        self.assertEqual(txn, Transaction(500, TransactionCategory.INCOME))

    def test_adapter_converts_expense(self):
        class ExternalExpense:
            amount = 75
            typ = "expense"

        txn = TransactionAdapter(ExternalExpense()).to_transaction()
        self.assertEqual(txn, Transaction(75, TransactionCategory.EXPENSE))

    def test_adapter_rejects_unknown_type(self):
        class ExternalUnknown:
            amount = 10
            typ = "refund"

        with self.assertRaises(ValueError):
            TransactionAdapter(ExternalUnknown()).to_transaction()

    def test_adapter_rejects_missing_type(self):
        class ExternalNoType:
            amount = 10

        with self.assertRaises(ValueError):
            TransactionAdapter(ExternalNoType()).to_transaction()

if __name__ == "__main__":
    unittest.main()
