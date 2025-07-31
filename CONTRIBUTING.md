# Contributing to Nira

Thank you for your interest in improving **Nira**. Please follow the guidelines below to help us review your contribution quickly.

## Getting started

1. Fork the repository and create your feature branch from `main`.
2. Install the dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for linting and formatting
pre-commit install  # sets up git hooks
```

## Coding standards

Run the linters and formatters before submitting a pull request. They are also
executed automatically on staged files via the installed pre-commit hook:

```bash
flake8
black --check .
isort --check .
```

## Running tests

Execute the unit tests to ensure everything works:

```bash
python -m unittest discover
```

If tests fail to run, you can explicitly specify the tests directory:

```bash
PYTHONPATH=. python -m unittest discover -s tests -p 'test_*.py' -v
```

## Submitting changes

1. Commit your changes with clear messages.
2. Push to your fork and open a pull request against this repository.
3. Ensure your pull request description explains the changes clearly.

We appreciate every contribution!
