"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction_factory import TransactionFactory
from transaction.external_income_transaction import ExternalFreelanceIncome


def main():
    print("Adding transactions...")

    balance = Balance.get_instance()
    balance.register_observer(PrintObserver())
    balance.register_observer(LowBalanceAlertObserver(threshold=100))

    # Create standard transactions
    transactions = [
        TransactionFactory.create("income", 100),
        TransactionFactory.create("expense", 50),
        TransactionFactory.income(200),
        TransactionFactory.expense(75),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(
        1200, "INV-98765", "Mobile App Project"
    )
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Apply every transaction to the singleton Balance; each application
    # notifies both registered observers (print + low-balance alert).
    for transaction in all_transactions:
        balance.apply_transaction(transaction)

    print(f"Final balance: {balance.get_balance():.2f}")


if __name__ == "__main__":
    main()
