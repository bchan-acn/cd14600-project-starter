import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_factory import TransactionFactory


class TestTransactionFactory(unittest.TestCase):

    def test_create_income(self):
        self.assertEqual(TransactionFactory.create("income", 100),
                         Transaction(100, TransactionCategory.INCOME))

    def test_create_expense_case_insensitive(self):
        self.assertEqual(TransactionFactory.create("EXPENSE", 40),
                         Transaction(40, TransactionCategory.EXPENSE))

    def test_shortcuts(self):
        self.assertEqual(TransactionFactory.income(5).category, TransactionCategory.INCOME)
        self.assertEqual(TransactionFactory.expense(5).category, TransactionCategory.EXPENSE)

    def test_unknown_kind_raises(self):
        with self.assertRaises(ValueError):
            TransactionFactory.create("gift", 10)

    def test_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            TransactionFactory.create("income", -1)


if __name__ == "__main__":
    unittest.main()
