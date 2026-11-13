# transaction_factory.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TransactionFactory:
    """Factory Method: creates Transaction objects from a category name."""

    _creators = {
        "income": lambda amount: Transaction(amount, TransactionCategory.INCOME),
        "expense": lambda amount: Transaction(amount, TransactionCategory.EXPENSE),
    }

    @classmethod
    def create(cls, kind, amount):
        """Create a Transaction of the given kind ('income' or 'expense')."""
        creator = cls._creators.get(str(kind).lower())
        if creator is None:
            raise ValueError(f"Unsupported transaction kind: {kind!r}")
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        return creator(amount)

    @classmethod
    def income(cls, amount):
        return cls.create("income", amount)

    @classmethod
    def expense(cls, amount):
        return cls.create("expense", amount)
