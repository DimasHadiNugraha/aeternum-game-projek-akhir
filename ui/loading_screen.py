from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, ProgressBar, Button, Static
from textual.reactive import reactive


loading_steps = [
    "Membangun dunia Aeternum...",
    "Menyusun peta mimpi...",
    "Mengaktifkan sistem lucid...",
    "Membuka gerbang mimpi...",
]


logo = r"""
 █████╗ ███████╗████████╗███████╗██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██║   ██║████╗ ████║
███████║█████╗     ██║   █████╗  ██████╔╝██╔██╗ ██║██║   ██║██╔████╔██║
██╔══██║██╔══╝     ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║██║╚██╔╝██║
██║  ██║███████╗   ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
"""


class LoadingScreen(Screen):
    progress = reactive(0)
    text_index = reactive(0)

    def compose(self) -> ComposeResult:
        with Vertical(id="loading"):
            yield Static(logo, id="logo")
            yield Static("AETERNUM", id="title")
            yield Static("☾ ✦ E T E R N A L  D R E A M ✦ ☽", id="subtitle")
            yield Static("", id="status")
            yield ProgressBar(total=100, show_percentage=True, id="bar")
            with Center(id="btn_wrap"):
                yield Button("Mulai Game", id="start_btn", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#status", Static).update(loading_steps[0])
        self.set_interval(0.08, self._advance)
        self.set_interval(0.9, self._change_text)

    def _advance(self) -> None:
        if self.progress < 100:
            self.progress += 1
            self.query_one(ProgressBar).advance(1)

    def _change_text(self) -> None:
        self.text_index = (self.text_index + 1) % len(loading_steps)
        self.query_one("#status", Static).update(loading_steps[self.text_index])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_btn":
            self.app.push_screen(MainScreen())


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Static(
                "MAIN SCREEN AETERNUM\n\nPetualangan dimulai di sini.",
                id="main_text",
            )
        yield Footer()


class AeternumApp(App):
    CSS = """
    Screen {
        background: #070b16;
    }

    #loading {
        width: 100%;
        height: 100%;
        content-align: center middle;
        padding: 1 4;
    }

    #top_image {
        width: 100%;
        color: #22d3ee;
        text-align: center;
        margin: 0 0 1 0;
    }

    #logo {
        width: 100%;
        color: #8b5cf6;
        text-align: center;
        margin: 0 0 1 0;
    }

    #title {
        width: 100%;
        color: #f5d0fe;
        text-align: center;
        text-style: bold;
        margin: 0;
    }

    #subtitle {
        width: 100%;
        color: #93c5fd;
        text-align: center;
        margin: 0 0 1 0;
    }

    #status {
        width: 100%;
        color: #e2e8f0;
        text-align: center;
        margin: 1 0;
    }

    #bar {
        width: 70%;
        min-width: 40;
        height: 1;
        margin: 1 0;
    }

    #btn_wrap {
        width: 100%;
        height: 3;
        content-align: center middle;
        margin: 1 0 0 0;
    }

    #start_btn {
        width: 26;
        height: 3;
        text-style: bold;
    }

    #start_btn:hover {
        background: #a855f7;
    }

    #main_text {
        width: 70%;
        border: round #8b5cf6;
        padding: 2;
        text-align: center;
        color: #e2e8f0;
    }
    """

    def on_mount(self) -> None:
        self.push_screen(LoadingScreen())


if __name__ == "__main__":
    AeternumApp().run()