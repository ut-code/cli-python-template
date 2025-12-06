import time
from enum import Enum
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from textual_app import run_textual

app = typer.Typer(
    name="demo",
    help="[bold blue]Typer + Rich[/bold blue] テンプレート :sparkles:",
    rich_markup_mode="rich",
    no_args_is_help=True,
)

console = Console()

class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Style(str, Enum):
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"


def version_callback(value: bool):
    """バージョン表示"""
    if value:
        console.print("[bold green]Demo CLI[/bold green] version [cyan]1.0.0[/cyan]")
        raise typer.Exit()


@app.callback()
def main(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="詳細出力を有効化"),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="バージョンを表示",
        ),
    ] = None,
):
    """
    グローバルオプション
    """
    if verbose:
        console.print("[dim]Verbose mode: ON[/dim]")


@app.command()
def hello(
    name: Annotated[str, typer.Argument(help="名前")],
    color: Annotated[
        Color, typer.Option("--color", "-c", help="色を選択")
    ] = Color.BLUE,
    style: Annotated[
        Style, typer.Option("--style", "-s", help="スタイルを選択")
    ] = Style.BOLD,
    count: Annotated[
        int, typer.Option("--count", "-n", min=1, max=10, help="回数 (1-10)")
    ] = 1,
    uppercase: Annotated[
        bool, typer.Option("--upper", "-u", help="大文字にする")
    ] = False,
):
    """
    [cyan]挨拶を表示[/cyan]
    """
    display_name = name.upper() if uppercase else name
    for _ in range(count):
        console.print(
            f"[{style.value} {color.value}]Hello, {display_name}![/{style.value} {color.value}]"
        )


@app.command()
def table(
    rows: Annotated[
        int, typer.Option("--rows", "-r", min=1, max=10, help="表示行数 (1-10)")
    ] = 4,
    border: Annotated[
        bool, typer.Option("--border", "-b", help="行間のボーダーを表示")
    ] = True,
):
    """
    [cyan]テーブル表示[/cyan]のデモ
    """
    tbl = Table(title="📊 ユーザー一覧", show_lines=border)

    tbl.add_column("ID", justify="right", style="cyan")
    tbl.add_column("名前", style="green")
    tbl.add_column("ステータス", justify="center")
    tbl.add_column("スコア", justify="right", style="yellow")

    data = [
        ("Alice", "✅ Active", "85.0"),
        ("Bob", "⏸️ Paused", "72.5"),
        ("Charlie", "❌ Stopped", "90.0"),
        ("Diana", "🔄 Running", "68.5"),
        ("Eve", "✅ Active", "95.0"),
        ("Frank", "⏸️ Paused", "60.0"),
        ("Grace", "🔄 Running", "78.5"),
        ("Henry", "❌ Stopped", "55.0"),
        ("Ivy", "✅ Active", "88.0"),
        ("Jack", "🔄 Running", "82.0"),
    ]

    for i, (name, status, score) in enumerate(data[:rows], 1):
        tbl.add_row(str(i), name, status, score)

    console.print(tbl)


@app.command()
def tree():
    """
    [cyan]ツリー表示[/cyan]のデモ
    """
    t = Tree("📁 [bold blue]project[/bold blue]")

    src = t.add("📁 [blue]src[/blue]")
    src.add("📄 [green]main.py[/green]")
    src.add("📄 [green]utils.py[/green]")

    tests = t.add("📁 [blue]tests[/blue]")
    tests.add("📄 [yellow]test_main.py[/yellow]")

    t.add("📄 [cyan]README.md[/cyan]")
    t.add("📄 [cyan]pyproject.toml[/cyan]")

    console.print(t)


@app.command()
def progress(
    seconds: Annotated[float, typer.Option("--seconds", "-s", help="秒数")] = 3.0,
):
    """
    [cyan]プログレスバー[/cyan]のデモ
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as prog:
        task = prog.add_task("Processing...", total=100)

        for _ in range(100):
            time.sleep(seconds / 100)
            prog.update(task, advance=1)

    console.print("[bold green]✅ Complete![/bold green]")


@app.command()
def code(
    lang: Annotated[str, typer.Option("--lang", "-l", help="言語")] = "python",
):
    """
    [cyan]シンタックスハイライト[/cyan]のデモ
    """
    samples = {
        "python": '''def greet(name: str) -> str:
    """挨拶を返す"""
    return f"Hello, {name}!"

print(greet("World"))
''',
        "javascript": """const greet = (name) => {
    return `Hello, ${name}!`;
};

console.log(greet("World"));
""",
    }

    src = samples.get(lang, samples["python"])
    syntax = Syntax(src, lang, theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"[bold]{lang}[/bold]", border_style="green"))


@app.command()
def confirm(
    message: Annotated[str, typer.Argument(help="メッセージ")] = "実行しますか？",
):
    """
    [cyan]確認プロンプト[/cyan]のデモ
    """
    if typer.confirm(message):
        console.print("[green]✅ 実行しました[/green]")
    else:
        console.print("[yellow]❌ キャンセルしました[/yellow]")
        raise typer.Abort()


@app.command()
def spinner(
    seconds: Annotated[float, typer.Option("--seconds", "-s", help="秒数")] = 2.0,
):
    """
    [cyan]スピナー[/cyan]のデモ
    """
    with console.status("[bold green]Loading...", spinner="dots"):
        time.sleep(seconds)

    console.print("[bold green]✅ Done![/bold green]")


@app.command()
def textual():
    """
    [cyan]Textual TUI[/cyan]のデモ
    """
    run_textual()

if __name__ == "__main__":
    app()
