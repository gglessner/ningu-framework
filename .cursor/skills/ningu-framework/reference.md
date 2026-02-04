# Ningu Framework Reference

Complete API reference, widget patterns, and Qt essentials.

---

## Recommended Module Structure

Use a separate UI class for better organization:

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont

TAB_LABEL = "MyModule v1.0.0"

class Ui_TabContent:
    def setupUi(self, widget):
        """Set up the UI components."""
        widget.setObjectName("TabContent")
        
        self.layout = QVBoxLayout(widget)
        
        self.titleLabel = QLabel(widget)
        font = QFont("Courier New", 14)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.layout.addWidget(self.titleLabel)
        
        self.actionButton = QPushButton(widget)
        self.actionButton.setText("Do Something")
        self.layout.addWidget(self.actionButton)
        
        self.retranslateUi(widget)
    
    def retranslateUi(self, widget):
        """Set text for UI elements."""
        self.titleLabel.setText("My Module")


class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TabContent()
        self.ui.setupUi(self)
        
        self.ui.actionButton.clicked.connect(self.on_action_clicked)
    
    def on_action_clicked(self):
        print("Button clicked!")
    
    def cleanup(self):
        pass
```

---

## Standard Layout Pattern

```
+--------------------------------------------------+
| Title/Header area                                |
| Input fields                                     |
+--------------------------------------------------+
|                                                  |
| Main content area                                |
| (tables, text boxes, lists)                      |
|                                                  |
+--------------------------------------------------+
| Status/Output (QPlainTextEdit, readonly)         |
+--------------------------------------------------+
```

---

## Qt Signal Patterns

### Common Signals

| Widget | Common Signals |
|--------|---------------|
| `QPushButton` | `clicked`, `pressed`, `released` |
| `QLineEdit` | `textChanged`, `returnPressed`, `editingFinished` |
| `QComboBox` | `currentIndexChanged`, `currentTextChanged` |
| `QCheckBox` | `stateChanged`, `toggled` |
| `QListWidget` | `itemClicked`, `itemSelectionChanged` |
| `QTableWidget` | `cellClicked`, `itemSelectionChanged` |
| `QPlainTextEdit` | `textChanged` |

### Connecting Signals

```python
# Direct connection
self.ui.myButton.clicked.connect(self.on_button_clicked)

# With lambda for parameters
self.ui.myButton.clicked.connect(lambda: self.do_something("param"))
```

---

## QThread Worker Pattern

```python
from PySide6.QtCore import QThread, Signal

class MyWorker(QThread):
    progress = Signal(int)      # Progress percentage
    result = Signal(dict)       # Result data
    error = Signal(str)         # Error message
    finished_work = Signal()    # Completion signal
    
    def __init__(self, input_data):
        super().__init__()
        self.input_data = input_data
        self._stop_requested = False
    
    def stop(self):
        self._stop_requested = True
    
    def run(self):
        try:
            for i, item in enumerate(self.input_data):
                if self._stop_requested:
                    return
                # Do work...
                self.progress.emit(int(100 * i / len(self.input_data)))
            
            self.result.emit({"status": "complete"})
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished_work.emit()
```

### Using the Worker

```python
class TabContent(QWidget):
    def start_work(self):
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        
        self.worker = MyWorker(self.data)
        self.worker.progress.connect(self.on_progress)
        self.worker.result.connect(self.on_result)
        self.worker.error.connect(self.on_error)
        self.worker.finished_work.connect(self.on_finished)
        self.worker.start()
    
    def stop_work(self):
        if self.worker:
            self.worker.stop()
    
    def cleanup(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait(5000)
```

---

## Checkable Buttons (Toggles)

```python
self.ui.myButton = QPushButton("Off")
self.ui.myButton.setCheckable(True)
self.ui.myButton.clicked.connect(self.on_toggle)

def on_toggle(self):
    if self.ui.myButton.isChecked():
        self.ui.myButton.setText("On")
    else:
        self.ui.myButton.setText("Off")
```

---

## showEvent Pattern

Run code when tab becomes visible:

```python
def showEvent(self, event):
    super().showEvent(event)
    self.ui.inputLine.setFocus()
```

---

## State Persistence

```python
import json
import os

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = os.path.join('modules', 'MyModule_config.json')
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.ui.inputLine.setText(config.get('last_input', ''))
            except Exception:
                pass
    
    def save_config(self):
        config = {'last_input': self.ui.inputLine.text()}
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
    
    def cleanup(self):
        self.save_config()
```

---

## Widget Enable/Disable Pattern

```python
def start_operation(self):
    self.ui.inputLine.setEnabled(False)
    self.ui.startButton.setEnabled(False)
    self.ui.stopButton.setEnabled(True)

def finish_operation(self):
    self.ui.inputLine.setEnabled(True)
    self.ui.startButton.setEnabled(True)
    self.ui.stopButton.setEnabled(False)
```

---

## Error Handling

```python
def process_data(self):
    try:
        result = risky_operation()
        self.ui.statusBox.appendPlainText(f"Success: {result}")
    except FileNotFoundError as e:
        self.ui.statusBox.appendPlainText(f"File not found: {e}")
    except PermissionError as e:
        self.ui.statusBox.appendPlainText(f"Permission denied: {e}")
    except Exception as e:
        import traceback
        print(f"Unexpected error: {traceback.format_exc()}")
        self.ui.statusBox.appendPlainText(f"Error: {e}")
```

---

## Socket and TLS Patterns

```python
import socket
import ssl

# TCP socket with SO_REUSEADDR
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)

# TLS client with optional verification skip
context = ssl.create_default_context()
if not verify_certificate:
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

tls_socket = context.wrap_socket(raw_socket, server_hostname=remote_host)
```

---

## Cross-Platform Best Practices

| Avoid | Use Instead |
|-------|-------------|
| Hardcoded `/` or `\` | `os.path.join()` or `Path()` |
| `os.system()` | `subprocess.run()` |
| Bare `open()` | `open(f, encoding='utf-8')` |
| `~` in paths | `os.path.expanduser("~")` |
| Hardcoded temp paths | `tempfile.gettempdir()` |

### Check Tool Availability

```python
import shutil

if shutil.which("openssl") is None:
    self.ui.statusBox.appendPlainText("ERROR: openssl not found")
    return
```

### Run External Commands

```python
import subprocess
import sys

# Hide console on Windows
startupinfo = None
if sys.platform == "win32":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

result = subprocess.run(
    ["command", "arg"],
    capture_output=True,
    startupinfo=startupinfo,
    timeout=10
)
```

---

## Common Pitfalls

| Error | Likely Cause |
|-------|--------------|
| `module 'X' lacks 'TabContent' class` | Missing or misspelled class |
| `'TabContent' is not a QWidget` | Doesn't inherit from QWidget |
| `AttributeError: 'Ui_TabContent' has no attribute 'X'` | Accessing UI before `setupUi()` |
| `RuntimeError: wrapped C/C++ object deleted` | Accessing destroyed widget |

---

## File Header Template

```python
# ModuleName - part of the Ningu Framework
# Copyright (C) 2025 Your Name - your@email.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
```
