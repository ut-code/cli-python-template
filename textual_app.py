from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    ProgressBar,
    Static,
    Switch,
)


class TextualApp(App):
    TITLE = "Textual Demo"
    SUB_TITLE = "template for CLI app with Textual"

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        width: 100%;
        height: 100%;
        padding: 1 2;
    }

    #table-section {
        height: 12;
        margin-bottom: 1;
    }

    DataTable {
        height: 100%;
    }

    #form-section {
        height: auto;
        margin-bottom: 1;
        padding: 1;
        border: solid $primary;
    }

    #form-title {
        text-style: bold;
        margin-bottom: 1;
    }

    .form-row {
        height: 3;
        margin-bottom: 1;
    }

    .form-row Label {
        width: 15;
        padding-top: 1;
    }

    .form-row Input {
        width: 1fr;
    }

    #button-row {
        height: 3;
        margin-top: 1;
    }

    Button {
        margin-right: 1;
    }

    #result {
        height: 3;
        margin-top: 1;
        padding: 1;
        background: $boost;
    }

    #progress-section {
        height: auto;
        padding: 1;
        border: solid $secondary;
    }

    #progress-title {
        text-style: bold;
        margin-bottom: 1;
    }

    ProgressBar {
        width: 100%;
        margin: 1 0;
    }

    #progress-buttons {
        height: 3;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "終了"),
        Binding("d", "toggle_dark", "ダーク/ライト"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="main-container"):
            with Vertical(id="table-section"):
                yield DataTable(id="data-table")

            with Vertical(id="form-section"):
                yield Static("� フォーム入力", id="form-title")
                with Horizontal(classes="form-row"):
                    yield Label("名前:")
                    yield Input(placeholder="名前を入力...", id="name-input")
                with Horizontal(classes="form-row"):
                    yield Label("メール:")
                    yield Input(placeholder="email@example.com", id="email-input")
                with Horizontal(classes="form-row"):
                    yield Label("通知:")
                    yield Switch(id="notify-switch")
                with Horizontal(id="button-row"):
                    yield Button("送信", variant="primary", id="submit-btn")
                    yield Button("クリア", variant="warning", id="clear-btn")
                yield Static("", id="result")

            with Vertical(id="progress-section"):
                yield Static("⏳ プログレスバー", id="progress-title")
                yield ProgressBar(id="progress-bar", total=100)
                with Horizontal(id="progress-buttons"):
                    yield Button("開始", variant="success", id="start-btn")
                    yield Button("リセット", variant="error", id="reset-btn")

        yield Footer()

    def on_mount(self) -> None:
        """アプリ起動時の初期化"""
        table = self.query_one("#data-table", DataTable)
        table.add_columns("ID", "名前", "ステータス", "スコア")
        table.add_rows(
            [
                ("1", "Alice", "✅ Active", "85.0"),
                ("2", "Bob", "⏸️ Paused", "72.5"),
                ("3", "Charlie", "❌ Stopped", "90.0"),
                ("4", "Diana", "🔄 Running", "68.5"),
            ]
        )
        table.cursor_type = "row"

    def action_toggle_dark(self) -> None:
        """ダーク/ライトモード切替"""
        self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """ボタンクリック処理"""
        if event.button.id == "submit-btn":
            name = self.query_one("#name-input", Input).value or "(未入力)"
            email = self.query_one("#email-input", Input).value or "(未入力)"
            notify = "ON" if self.query_one("#notify-switch", Switch).value else "OFF"
            result = self.query_one("#result", Static)
            result.update(f"✅ 送信完了! 名前: {name}, Email: {email}, 通知: {notify}")

        elif event.button.id == "clear-btn":
            self.query_one("#name-input", Input).value = ""
            self.query_one("#email-input", Input).value = ""
            self.query_one("#notify-switch", Switch).value = False
            self.query_one("#result", Static).update("")

        elif event.button.id == "start-btn":
            progress = self.query_one("#progress-bar", ProgressBar)
            progress.update(progress=0)
            self.run_progress()

        elif event.button.id == "reset-btn":
            self.query_one("#progress-bar", ProgressBar).update(progress=0)

    def run_progress(self) -> None:
        """プログレスバーのアニメーション"""
        self.set_interval(0.05, self._update_progress, name="progress_timer")

    def _update_progress(self) -> None:
        """プログレス更新"""
        progress = self.query_one("#progress-bar", ProgressBar)
        if progress.progress is not None and progress.progress < 100:
            progress.advance(2)
        else:
            for timer in self._timers:
                if timer.name == "progress_timer":
                    timer.stop()
                    break


def run_textual():
    """デモアプリを起動"""
    app = TextualApp()
    app.run()
