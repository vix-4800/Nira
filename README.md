# Nira

A simple command execution assistant that uses an LLM backend.

## Installation

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies with:

```bash
pip install -r requirements.txt
```

## Configuration

`main.py` reads environment variables to determine the server URL and model to use. These can be provided directly in the environment or via a `.env` file.

Example `.env`:

```
SERVER=http://localhost:11434
MODEL=qwen3:4b
AUTO_CONFIRM=false
```

Run the application with:

```
python main.py
```

The default server is `http://localhost:11434` and the default model is `qwen3:4b` if the variables are not set.

By default all commands, prompts and responses are logged to a timestamped file under the `logs/` directory. You can override the location with the `--log-file` argument.

Set `AUTO_CONFIRM` to `true` in the environment to run safe commands without confirmation. Dangerous commands are always confirmed explicitly.

## Running tests

Install the dependencies and run:

```bash
python -m unittest discover
```

All tests are executed automatically on GitHub for every push and pull request.

## License

This project is licensed under the [MIT License](LICENSE).
