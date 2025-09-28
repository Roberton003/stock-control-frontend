
# Project Status

The project is still in a refactoring phase. The main goal is to have a clean test run before adding new features.

## Current Issues

| Issue | File(s) | Description | Attempts | Plan |
| :--- | :--- | :--- | :--- | :--- |
| `IndentationError` | `e2e_tests/test_ui.py`, `inventory/tests/test_reports_api.py` | The tests are failing due to an `IndentationError`. | I have tried to fix the indentation multiple times, but it seems I'm missing something. | I will carefully read the files and fix the indentation issues. |
| `KeyError: 'location__name'` | `e2e_tests/test_ui.py`, `inventory/tests/test_reports_api.py` | The `get_stock_value_report` service is not returning the `location__name` field. | I have tried to fix the service and the tests, but it seems I'm still using the wrong key. | I will fix the service to return the correct key and update the tests accordingly. |
| `AttributeError: 'method_descriptor' object has no attribute 'today'` | `inventory/views.py` | The `DashboardSummaryView` is using `datetime.date.today` instead of `datetime.date.today()`. | I have tried to fix this multiple times, but the error persists. | I will replace all occurrences of `datetime.date.today` with `datetime.date.today()`. |
| Performance test failures | `inventory/tests/test_performance.py` | The performance tests are failing with an `AssertionError`. | I have ignored these tests for now to focus on the functional issues. | I will keep ignoring them for now and will address them after the functional tests are passing. |
