# Personal Finance Manager — Design Patterns Project

This project is a hands-on exercise in applying Object-Oriented Design Patterns to build a simplified personal finance manager.
You will implement and extend starter code to add functionality such as tracking transactions, adapting external data, observing balance changes, and ensuring proper architectural patterns.

## Getting Started

### Dependencies

Make sure you have python version >= 3.10.x installed on your computer. 


### Installation

1. Clone the repo:

```
bash
git clone https://github.com/udacity/cd14600-project-starter.git
cd cd14600-project-starter/starter
```

2. Run the Program: 
```
python main.py
```

## Testing

This project uses Python’s built-in unittest framework.

To run all tests:

```
python -m unittest discover
```

To run a single test file:
```
python -m unittest balance/test_balance_observer.py
```

### Break Down Tests

- test_balance.py → Verifies correct implementation of the Singleton Balance class.
- test_transaction.py → Confirms transactions update balances correctly.
- test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.
- test_balance_observer.py → Validates that low-balance alerts are triggered at the correct threshold.

## Project Instructions

1. Implement Singleton Balance Class – Ensure only one balance object exists throughout the app.
2. Complete Transaction Class – Handle income and expense transactions.
3. Implement Adapter Pattern – Adapt external freelance income data into internal Transaction objects.
4. Implement Observer Pattern – Create a low balance observer that triggers an alert when funds drop too low.
5. Add Unit Tests – Write tests for all implemented functionality.
6. Choose and Implement a Fourth Pattern – Pick one additional design pattern (e.g., Strategy, Command, Decorator, etc.) and integrate it into your project.
7. Provide a Reflection – Add a short write-up in your repo (README or separate file) explaining your design choices.

## Built With

* [Python](https://www.python.org/) – Main programming language
* [unittest](https://docs.python.org/3/library/unittest.html) – Testing framework
* [PEP8](https://peps.python.org/pep-0008/) – Style guide for Python code

## License

[License](LICENSE.txt)

## Provide a Reflection

This project combines four design patterns. Each one solves a specific problem, and each has a cost.

### Singleton: `Balance`

- **Role:** `Balance` uses `__new__` and `get_instance()` so the whole app shares one net balance.
- **Benefit:** Every component reads and updates the same state. Nothing has to pass a balance object around.
- **Trade-off:** Shared state carries over between tests, so every test's `setUp` must call `reset()`. `reset()` only zeroes the amount. It does not clear `_observers`, so observers registered in one test can still be attached in the next. Global state is convenient but makes test isolation harder.

### Adapter: `TransactionAdapter`

- **Role:** It converts an external record, such as `ExternalFreelanceIncome`, into the project's own `Transaction`.
- **Benefit:** `Balance` only knows about `Transaction`. A new third-party format needs a new adapter, not changes to `Balance`.
- **Trade-off:** The adapter keeps only the amount and category. It drops `invoice_id` and `description`, so that metadata is lost. An unknown `typ` raises a `ValueError`, so every new external type needs explicit support.

### Observer: `IBalanceObserver`, `PrintObserver`, `LowBalanceAlertObserver`

- **Role:** After each `apply_transaction`, `Balance` notifies its registered observers.
- **Benefit:** Logging and low-balance alerts are added without editing `Balance`. Observers can be added or removed independently.
- **Trade-off:** Observers need lifecycle management. One that is never unregistered keeps firing. Notifications only happen through `apply_transaction`, so calling `add_income` or `add_expense` directly bypasses them. `LowBalanceAlertObserver` also alerts on every transaction while the balance stays below the threshold, not just once.

### Factory Method: `TransactionFactory`

A Factory Method fits because it puts creation in one place:

- It is easy to extend.
    - A new transaction kind, such as a refund or transfer, is one new entry in the factory's creators table. Balance, the adapter and the observers don't change.

- It complements the Adapter.
    - The Adapter converts external data into a Transaction. The Factory is the single way to create internal ones. Together, every Transaction comes from a controlled path.

- **Trade-off:** Kinds are looked up by string, so a typo fails at runtime with a `ValueError`, not when the code is loaded. With only two kinds, the factory is also a thin wrapper around the `Transaction` constructor, and its value shows up only as more kinds are added.

### How they fit together

The Adapter and the Factory are the two ways a `Transaction` is created. The Singleton `Balance` applies it, and the Observers react to the result.
