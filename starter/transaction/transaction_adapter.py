# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TransactionAdapter:
    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external transaction to a standard Transaction."""
        typ = getattr(self.external_transaction, "typ", None)
        if typ == "income":
            category = TransactionCategory.INCOME
        elif typ == "expense":
            category = TransactionCategory.EXPENSE
        else:
            raise ValueError(f"Unsupported external transaction type: {typ!r}")
        return Transaction(self.external_transaction.amount, category)
