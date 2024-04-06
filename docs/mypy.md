### File describe work with mypy

typing check:

```bash
mypy .
mypy -p /path/to/directory
mypy -m /path/to/file.ext
```

stub package installation example:

```bash
pip install types-PyYAML types-requests
```

ignore:

```bash
# type: ignore
# type: ignore[<error-code>]
```

link to docs [mypy](https://mypy.readthedocs.io/en/stable/index.html)
