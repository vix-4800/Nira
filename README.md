# Nexora

A simple command execution assistant that uses an LLM backend.

## Configuration

`main.py` reads environment variables to determine the server URL and model to use. These can be provided directly in the environment or via a `.env` file.

Example `.env`:

```
SERVER=http://localhost:11434
MODEL=qwen3:4b
```

Run the application with:

```
python main.py
```

The default server is `http://localhost:11434` and the default model is `qwen3:4b` if the variables are not set.
