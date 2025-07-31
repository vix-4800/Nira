# Nira

A simple command execution assistant that uses an LLM backend.
Responses are displayed using Rich's Markdown renderer, allowing formatted output.

## Installation

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies with:

```bash
pip install -r requirements.txt
```

3. (Optional) Install development dependencies for linting and formatting:

```bash
pip install -r requirements-dev.txt
```

## Configuration

`main.py` reads environment variables to determine the server URL and model to use. These can be provided directly in the environment or via a `.env` file.

Example `.env`:

```ini
SERVER=http://localhost:11434
MODEL=qwen3:4b
AUTO_CONFIRM=false
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
OBSIDIAN_VAULT=
GITHUB_TOKEN=
DNS_SERVER=
TODOIST_TOKEN=
```

`TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are required for the Telegram tool to send messages.
`GITHUB_TOKEN` is optional and is used by the GitHub tool for authenticated requests.
`TODOIST_TOKEN` is required for the Todoist tool to manage tasks.
`OBSIDIAN_VAULT` should point to the directory containing your Obsidian notes and is required for the Obsidian tools.
`DNS_SERVER` is optional and overrides the DNS server used for domain lookups.

Run the application with:

```bash
python main.py
```

Use `/exit`, `Ctrl+C` or `Ctrl+D` to quit the application gracefully.

The default server is `http://localhost:11434` and the default model is `qwen3:4b` if the variables are not set.

By default all commands, prompts and responses are logged to a JSON file named `chat.log` in the current directory.

Set `AUTO_CONFIRM` to `true` in the environment to run safe commands without confirmation. Any command recognised as dangerous (like `rm -rf`, `shutdown`, or `poweroff`) will always require explicit confirmation before execution.

Prometheus metrics are exposed on port `8000` by default, providing `tools_called_total` and `tool_error_total` counters. Set the `METRICS_PORT` environment variable to change the port.

The assistant now maintains conversational context using LangChain's conversation memory. This allows you to chat naturally and refer back to previous questions in the same session.

## Development

Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the linters and formatters:

```bash
flake8
black --check .
isort --check .
```

## Running tests

Install the dependencies and run:
Dependencies from `requirements.txt` must be installed prior to running `python -m unittest discover`.

```bash
python -m unittest discover
```

All tests are executed automatically on GitHub for every push and pull request.

## License

This project is licensed under the [MIT License](LICENSE).
