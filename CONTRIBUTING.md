# Contributing

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pip install -r requirements-dev.txt
```

## Checks

```bash
ruff check .
pytest -q
```

## PR guidelines

- Keep changes small and focused
- Add/extend tests when changing behavior
- Avoid committing large datasets to git (use `data/` which is gitignored)
