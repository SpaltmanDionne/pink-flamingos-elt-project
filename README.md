# ELT project by the Pink Flamingos

Team members: Arthur, Yossi, Sarah & Dionne 

## Steps to set up airflow 
- Go to the Airflow folder
- Run in your command line: `docker compose up --build -d`
- Minio: http://localhost:9001/ 
- Airflow: http://localhost:8080/ 


## Steps to run docker 
Command to start up your docker-compose: 

```bash
docker compose up --build -d 
```
```bash
docker compose down
```

## Installing UV

[UV](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver, written in Rust. It's designed as a drop-in replacement for pip and pip-tools.

### Installation

### macOS and Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


### Verify Installation

```bash
uv --version
```

### Add dependencies

```bash
uv add ruff
```

This will:
- Create a `pyproject.toml` if it doesn't exist
- Add ruff to your project dependencies
- Update your lockfile

### Sync dependencies

Install all project dependencies:

```bash
uv sync
```

This creates a virtual environment in `.venv` and installs all dependencies.

### Activate the virtual environment

#### macOS/Linux

```bash
source .venv/bin/activate
```

### 5. Run tools

With the virtual environment activated:

```bash
ruff check
```

Or run directly without activating:

```bash
uv run ruff check
```

### Common Commands

| Command | Description |
|---------|-------------|
| `uv add <package>` | Add a dependency to your project |
| `uv remove <package>` | Remove a dependency |
| `uv sync` | Install all dependencies from lockfile |
| `uv run <command>` | Run a command in the project environment |
| `uv pip install <package>` | Install package (pip-compatible) |
| `uv pip list` | List installed packages |

### Tips

- UV automatically manages your virtual environment
- Use `uv run` to execute commands without activating the venv
- UV is much faster than pip for dependency resolution
- It uses a global cache to speed up installations across projects