# Ningu Module Examples

Complete, copy-paste ready module templates.

---

## Minimum Viable Module

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

TAB_LABEL = "MyModule"

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Hello World"))
```

---

## Complete Module with Input/Output

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QPlainTextEdit, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

VERSION = "1.0.0"
TAB_LABEL = f"MyModule v{VERSION}"


class Ui_TabContent:
    def setupUi(self, widget):
        widget.setObjectName("TabContent")
        
        self.mainLayout = QVBoxLayout(widget)
        self.mainLayout.setSpacing(5)
        
        # Title
        self.titleLabel = QLabel(widget)
        font = QFont("Courier New", 12)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setText(f"MyModule v{VERSION}")
        self.mainLayout.addWidget(self.titleLabel)
        
        # Input area
        self.inputFrame = QFrame(widget)
        self.inputLayout = QHBoxLayout(self.inputFrame)
        
        self.inputLabel = QLabel("Input:")
        self.inputLayout.addWidget(self.inputLabel)
        
        self.inputLine = QLineEdit()
        self.inputLayout.addWidget(self.inputLine)
        
        self.processButton = QPushButton("Process")
        self.inputLayout.addWidget(self.processButton)
        
        self.mainLayout.addWidget(self.inputFrame)
        
        # Output area
        self.outputBox = QPlainTextEdit(widget)
        self.outputBox.setReadOnly(True)
        self.mainLayout.addWidget(self.outputBox)


class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TabContent()
        self.ui.setupUi(self)
        
        self.ui.processButton.clicked.connect(self.process_input)
        self.ui.inputLine.returnPressed.connect(self.process_input)
    
    def process_input(self):
        text = self.ui.inputLine.text()
        if text:
            self.ui.outputBox.appendPlainText(f"Processing: {text}")
            self.ui.inputLine.clear()
    
    def cleanup(self):
        pass
```

---

## Complete Module with Worker Thread

Production-ready template with background processing:

```python
# N_MyModule.py - A Ningu Framework Module
# Copyright (C) 2025 Your Name - your@email.com
# License: GPL v3

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QPlainTextEdit, QFrame,
    QProgressBar
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal
import os

VERSION = "1.0.0"
TAB_LABEL = f"MyModule v{VERSION}"


class Worker(QThread):
    """Background worker thread."""
    progress = Signal(str)
    finished_work = Signal()
    
    def __init__(self, input_data):
        super().__init__()
        self.input_data = input_data
        self._stop = False
    
    def stop(self):
        self._stop = True
    
    def run(self):
        self.progress.emit(f"Processing {len(self.input_data)} items...")
        for i, item in enumerate(self.input_data):
            if self._stop:
                self.progress.emit("Stopped by user")
                break
            # Do work here
            self.progress.emit(f"Item {i+1}: {item}")
        self.finished_work.emit()


class Ui_TabContent:
    def setupUi(self, widget):
        widget.setObjectName("TabContent")
        
        self.mainLayout = QVBoxLayout(widget)
        self.mainLayout.setSpacing(5)
        
        # Title
        self.titleLabel = QLabel(f"MyModule v{VERSION}")
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        self.titleLabel.setFont(font)
        self.mainLayout.addWidget(self.titleLabel)
        
        # Input frame
        self.inputFrame = QFrame()
        self.inputLayout = QHBoxLayout(self.inputFrame)
        
        self.inputLine = QLineEdit()
        self.inputLine.setPlaceholderText("Enter input...")
        self.inputLayout.addWidget(self.inputLine)
        
        self.startButton = QPushButton("Start")
        self.inputLayout.addWidget(self.startButton)
        
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        self.inputLayout.addWidget(self.stopButton)
        
        self.mainLayout.addWidget(self.inputFrame)
        
        # Progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 0)  # Indeterminate
        self.progressBar.setVisible(False)
        self.mainLayout.addWidget(self.progressBar)
        
        # Output
        self.outputBox = QPlainTextEdit()
        self.outputBox.setReadOnly(True)
        self.mainLayout.addWidget(self.outputBox)


class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TabContent()
        self.ui.setupUi(self)
        self.worker = None
        
        self.ui.startButton.clicked.connect(self.start_work)
        self.ui.stopButton.clicked.connect(self.stop_work)
        self.ui.inputLine.returnPressed.connect(self.start_work)
    
    def start_work(self):
        text = self.ui.inputLine.text().strip()
        if not text:
            self.ui.outputBox.appendPlainText("Please enter input")
            return
        
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.ui.progressBar.setVisible(True)
        
        self.worker = Worker(text.split())
        self.worker.progress.connect(self.on_progress)
        self.worker.finished_work.connect(self.on_finished)
        self.worker.start()
    
    def stop_work(self):
        if self.worker:
            self.worker.stop()
    
    def on_progress(self, message):
        self.ui.outputBox.appendPlainText(message)
    
    def on_finished(self):
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        self.ui.progressBar.setVisible(False)
        self.ui.outputBox.appendPlainText("Done!")
        self.worker = None
    
    def cleanup(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait(5000)
```

---

## Parley Sub-Module Example

```python
# Parley_modules_client/Display_Client_MyProtocol.py

from datetime import datetime
from log_utils import write_to_log

module_description = "decode and display MyProtocol client messages"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):
    # Check if this is our protocol
    if b'MYPROTO' not in message_data:
        return message_data
    
    # Build output
    output = []
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] "
                  f"{datetime.now().isoformat()} ------- Client ({message_num}) -------")
    output.append(f"Data: {message_data.hex()}")
    full_output = '\n'.join(output)
    
    print(full_output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)
    
    return message_data
```

---

## SecretDecoderRing Sub-Module Example

```python
# SecretDecoderRing_modules/MyEncryption_v1.0.py

from Crypto.Cipher import AES

def decrypt(iv, key, ciphertext):
    results = []
    
    # Try ECB mode
    try:
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        results.append(("AES-ECB", plaintext))
    except Exception:
        pass
    
    # Try CBC mode
    if iv and len(iv) == 16:
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = cipher.decrypt(ciphertext)
            results.append(("AES-CBC", plaintext))
        except Exception:
            pass
    
    return results
```

---

## AuthCheck Sub-Module Example

```python
# AuthCheck_modules/MyAuth.py

import requests

module_description = "Test authentication against MyService API"

form_fields = [
    {
        'name': 'host',
        'type': 'text',
        'label': 'API Host',
        'default': 'api.example.com'
    },
    {
        'name': 'port',
        'type': 'text',
        'label': 'Port',
        'default': '443',
        'port_toggle': 'use_tls',
        'tls_port': '443',
        'non_tls_port': '80'
    },
    {
        'name': 'username',
        'type': 'text',
        'label': 'Username',
        'default': ''
    },
    {
        'name': 'password',
        'type': 'password',
        'label': 'Password',
        'default': ''
    },
    {
        'name': 'use_tls',
        'type': 'checkbox',
        'label': 'Use HTTPS',
        'default': True
    }
]

def authenticate(form_data):
    host = form_data.get('host', '')
    port = form_data.get('port', '443')
    username = form_data.get('username', '')
    password = form_data.get('password', '')
    use_tls = form_data.get('use_tls', True)
    
    protocol = 'https' if use_tls else 'http'
    url = f"{protocol}://{host}:{port}/api/auth"
    
    try:
        response = requests.post(
            url,
            json={'username': username, 'password': password},
            timeout=10,
            verify=use_tls
        )
        
        if response.status_code == 200:
            return True, f"Authenticated as {username}"
        elif response.status_code == 401:
            return False, "Invalid credentials"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    
    except requests.exceptions.Timeout:
        return False, "Connection timed out"
    except requests.exceptions.ConnectionError as e:
        return False, f"Connection failed: {e}"
    except Exception as e:
        return False, f"Error: {e}"
```

---

## Module with Sub-Module Loading

```python
import importlib.util
import os

VERSION = "1.0.0"
TAB_LABEL = f"MyModule v{VERSION}"


class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.submodules = []
        self.load_submodules()
    
    def load_submodules(self):
        """Load sub-modules from directory."""
        modules_dir = os.path.join('modules', 'MyModule_submodules')
        
        if not os.path.isdir(modules_dir):
            os.makedirs(modules_dir, exist_ok=True)
            return
        
        for filename in sorted(os.listdir(modules_dir)):
            if filename.endswith('.py') and filename != '__init__.py':
                file_path = os.path.join(modules_dir, filename)
                spec = importlib.util.spec_from_file_location(
                    filename[:-3], file_path
                )
                
                if spec is None or spec.loader is None:
                    continue
                
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'process'):
                        self.submodules.append({
                            'name': filename[:-3],
                            'module': module,
                            'description': getattr(
                                module, 'module_description', ''
                            )
                        })
                
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
```
