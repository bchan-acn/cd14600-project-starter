# balance.py

from transaction.transaction_category import TransactionCategory

class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._balance = 0.0
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Return the shared balance manager."""
        return cls()

    def reset(self):
        """Reset the net balance to zero."""
        self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self._balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError("Invalid transaction category")

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net balance: {self._balance:.2f}"
    
