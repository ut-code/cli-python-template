# 環境構築

uvをインストール: https://docs.astral.sh/uv/getting-started/installation/
もしくはnixを使う

```bash
uv init cli-python-template
cd cli-python-template
uv add typer rich textual
uv add --dev ruff
```
main.py と textual.py を作ってコードを貼り付ける

# 開発用コマンド

```bash
# lint
uv run ruff check --fix
uv run ruff check --watch
# format
uv run ruff format
# type check
uvx ty
# execute
uv run main.py
```
# 備考

- VS Code で >Python: Select Interpreter から ./.venv/bin/python を指定してパッケージを認識させる

# 参考

https://docs.astral.sh/uv/
https://docs.astral.sh/ruff/
https://typer.tiangolo.com/
https://rich.readthedocs.io/en/latest/
