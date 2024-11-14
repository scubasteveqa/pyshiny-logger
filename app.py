import multiprocessing
import pandas as pd
import platform
import psutil
import subprocess
import sys

from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.input_text_area("logme", "Text to log", placeholder="Enter text"),
    ui.input_checkbox("stderr", "log to stderr", False),
    ui.input_action_button("log_button", "Log"),
    ui.output_text_verbatim("logged"),
)


def server(input, output, session):
    @reactive.event(input.log_button)
    def logged():
        l = input.logme()
        if input.stderr():
            print(l, file=sys.stderr)
        else:
            print(l)
        return l

app = App(app_ui, server)

def run(input: list[str]) -> str:
    try:
        return subprocess.check_output(input).decode("utf-8").strip()
    except Exception as e:
        return f"Error: {e}"
