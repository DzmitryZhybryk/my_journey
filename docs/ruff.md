### File describe work with linter ruff

linter check:

```bash
ruff check .
ruff check . --fix
```

ignore:

```bash
[tool.ruff.lint]
ignore = ["F401"]
# ruff: noqa
# ruff: noqa: {code}
# ruff: noqa: D104
```

check and fix unused noqa:

```bash
ruff check /path/to/file.py --extend-select RUF100
ruff check /path/to/file.py --extend-select RUF100 --fix
```

formatter:

```bash
ruff format .
ruff format . --check
```

ignore:

```bash
# fmt: off
# fmt: on
# fmt: skip
```

for import sort:

```bash
ruff check --select I --fix .
ruff format .
```

link to docs [ruff](https://docs.astral.sh/ruff/)