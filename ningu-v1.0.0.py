#!/usr/bin/env python3

# Ningu (忍具) Framework
# Copyright (C) 2025 <Your Name or Organization>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""This is the main GUI element of the 忍具 framework"""

import os
import sys
import signal
import importlib.util
import re

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QTabWidget, QWidget, QMainWindow

def get_program_info():
    """Extract program name and version from the script filename."""
    filename = os.path.basename(__file__)
    name_version = os.path.splitext(filename)[0]
    match = re.match(r"(.+)-v([\d.]+)", name_version)
    if match:
        program_name, version = match.groups()
    else:
        program_name = name_version
        version = "1.0"
    return program_name, version

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        program_name, version = get_program_info()
        self.setWindowTitle(f"{program_name} v{version}")

        self.tabs = QTabWidget()
        bar = self.tabs.tabBar()
        bar.setExpanding(False)

        self.tabs.setStyleSheet("QTabWidget::tab-bar { alignment: left; }")

        self.setCentralWidget(self.tabs)
        self.widgets = []  # Track widgets for cleanup
        self.load_modules()

    def load_modules(self) -> None:
        module_dir = "modules"
        os.makedirs(module_dir, exist_ok=True)

        if not os.path.isdir(module_dir):
            print(f"Error: directory '{module_dir}' does not exist.")
            return

        for fname in sorted(
            f for f in os.listdir(module_dir)
            if f.endswith(".py") and f != "__init__.py"
        ):
            path = os.path.join(module_dir, fname)
            spec = importlib.util.spec_from_file_location(fname[:-3], path)
            if spec is None or spec.loader is None:
                print(f"Error: cannot create loader for '{fname}'.")
                continue

            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                if hasattr(module, "TabContent"):
                    widget = module.TabContent()
                    if isinstance(widget, QWidget):
                        tab_label = getattr(module, "TAB_LABEL", fname[:-3])
                        self.tabs.addTab(widget, tab_label)
                        self.widgets.append(widget)  # Store widget for cleanup
                    else:
                        print(f"Error: 'TabContent' in '{fname}' is not a QWidget.")
                else:
                    print(f"Error: module '{fname}' lacks a 'TabContent' class.")
            except Exception as exc:
                print(f"Error loading '{fname}': {exc}")

    def closeEvent(self, event):
        """Handle window close event to clean up resources."""
        for widget in self.widgets:
            if hasattr(widget, 'cleanup'):
                try:
                    widget.cleanup()
                except Exception as e:
                    print(f"Error cleaning up widget: {e}")
        event.accept()

# ----------------------------- main -----------------------------
def main() -> None:
    app = QApplication(sys.argv)

    interrupted = {"flag": False}

    def sigint_handler(*_):
        interrupted["flag"] = True
        app.quit()

    signal.signal(signal.SIGINT, sigint_handler)

    keep_alive = QTimer()
    keep_alive.start(100)
    keep_alive.timeout.connect(lambda: None)

    win = MainWindow()
    win.showMaximized()

    app.exec()
    if interrupted["flag"]:
        print("\nInterrupted by user")
    sys.exit(0)

if __name__ == "__main__":
    main()