# Ningu Module Development Guide

This document explains how to create modules for the Ningu Framework. It is designed to provide all necessary information for developing new modules that integrate seamlessly with the framework.

---

## Table of Contents

### Getting Started
1. [Framework Overview](#framework-overview)
2. [Required Module Structure](#required-module-structure)
3. [Tab Ordering](#tab-ordering)
4. [The TabContent Class](#the-tabcontent-class)
5. [Complete Minimal Example](#complete-minimal-example)

### UI Development
6. [UI Patterns](#ui-patterns)
7. [Qt/PySide6 Essentials](#qtpyside6-essentials)

### Module Lifecycle
8. [The cleanup() Method](#the-cleanup-method)
9. [Common Pitfalls and Gotchas](#common-pitfalls-and-gotchas)
10. [Advanced Widget Patterns](#advanced-widget-patterns)
11. [Debugging Tips](#debugging-tips)

### Complex Modules
12. [Module Directory Structure](#module-directory-structure)
13. [Shared Libraries (module_libs)](#shared-libraries-module_libs)
14. [Advanced: Sub-Module Support](#advanced-sub-module-support)

### Distribution
15. [Requirements.txt](#requirementstxt)
16. [README.md](#readmemd)
17. [Cross-Platform Development](#cross-platform-development)
18. [Code Style Conventions](#code-style-conventions)
19. [Integrating Standalone Modules](#integrating-standalone-modules)

### Reference
20. [Existing Module Examples](#existing-module-examples)
21. [Template: Complete Module with Worker Thread](#template-complete-module-with-worker-thread)
22. [Important Development Guidelines](#important-development-guidelines)
23. [Summary Checklist](#summary-checklist)
24. [Framework Source Reference](#framework-source-reference)
25. [Quick Reference](#quick-reference)
26. [Lessons Learned](#lessons-learned-real-development-examples)

---

## Framework Overview

Ningu is a PySide6-based GUI framework that dynamically loads Python modules from the `modules/` directory. Each module appears as a tab in the main application window.

**Key characteristics:**
- Modules are Python files (`.py`) in the `modules/` directory
- Files named `__init__.py` are ignored
- Modules are loaded in sorted order (filenames determine tab order)
- Each module must export a `TabContent` class that inherits from `QWidget`

---

## Required Module Structure

Every Ningu module **MUST** have:

### 1. `TabContent` Class (Required)
A class named exactly `TabContent` that inherits from `PySide6.QtWidgets.QWidget`.

```python
from PySide6.QtWidgets import QWidget

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        # Your initialization here
```

### 2. `TAB_LABEL` Variable (Optional but Recommended)
A string that defines the tab's display name. If not provided, the filename (without `.py`) is used.

```python
TAB_LABEL = "My Module v1.0.0"
```

---

## Tab Ordering

Tabs appear in **alphabetically sorted order** based on filename. Use numeric prefixes to control ordering:

| Filename | Tab Position |
|----------|-------------|
| `1_FirstModule.py` | 1st |
| `2_SecondModule.py` | 2nd |
| `3_Parley.py` | 3rd |
| `4_SecretDecoderRing.py` | 4th |
| `5_AuthCheck.py` | 5th |
| `ZZ_LastModule.py` | Last |

**Convention:** Use `N_ModuleName.py` format where `N` is a number.

---

## The TabContent Class

### Minimum Implementation

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

TAB_LABEL = "My Module"

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        label = QLabel("Hello from My Module!")
        layout.addWidget(label)
```

### Recommended Implementation

For better organization, use a separate UI class:

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont

TAB_LABEL = "My Module v1.0.0"

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
        """Set text for UI elements (for internationalization support)."""
        self.titleLabel.setText("My Module")


class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TabContent()
        self.ui.setupUi(self)
        
        # Connect signals to slots
        self.ui.actionButton.clicked.connect(self.on_action_clicked)
    
    def on_action_clicked(self):
        print("Button clicked!")
    
    def cleanup(self):
        """Clean up resources when the application closes."""
        pass
```

---

## UI Patterns

### Standard Layout Structure

Most Ningu modules follow this general layout pattern:

```
+--------------------------------------------------+
|  Title/Header area                               |
|  Input fields (often right-aligned)              |
+--------------------------------------------------+
|                                                  |
|  Main content area                               |
|  (tables, text boxes, lists, etc.)               |
|                                                  |
+--------------------------------------------------+
|  Status/Output window (QPlainTextEdit, readonly) |
+--------------------------------------------------+
```

**Note:** This is just a common pattern, not a requirement. Design your UI to fit your module's purpose.

### Common Widgets Used

| Widget | Purpose |
|--------|---------|
| `QPlainTextEdit` | Multi-line text input/output |
| `QLineEdit` | Single-line text input |
| `QPushButton` | Buttons (can be checkable for toggles) |
| `QComboBox` | Dropdown selections |
| `QTableWidget` | Results tables |
| `QListWidget` | Selectable lists |
| `QFrame` | Container for grouping widgets |
| `QLabel` | Text labels |

### Title/Header (Optional Stylistic Choice)

Some existing modules display ASCII art banners in the header. **This is purely a stylistic choice, not a requirement.** A simple text label works just as well:

```python
# Simple approach - just a title label
self.titleLabel = QLabel(widget)
self.titleLabel.setText("MyModule v1.0.0")

# Or with some styling
font = QFont()
font.setBold(True)
font.setPointSize(12)
self.titleLabel.setFont(font)
```

If you do want ASCII art (optional):

```python
self.titleLabel = QLabel(widget)
font = QFont("Courier New", 14)
font.setBold(True)
self.titleLabel.setFont(font)
self.titleLabel.setText("""
 __  __           _       _      
|  \\/  | ___   __| |_   _| | ___ 
| |\\/| |/ _ \\ / _` | | | | |/ _ \\
| |  | | (_) | (_| | |_| | |  __/
|_|  |_|\\___/ \\__,_|\\__,_|_|\\___|

Version: 1.0.0""")
```

---

## The cleanup() Method

The `cleanup()` method is called by the framework when the main window is closed. Use it to:

- Stop background threads
- Close open files/connections
- Release resources
- Save state

```python
class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.log_files = {}
    
    def cleanup(self):
        """Clean up resources on close."""
        # Stop worker threads
        if self.worker_thread:
            self.worker_thread.stop()
            self.worker_thread.wait()
        
        # Close open files
        for f in self.log_files.values():
            f.close()
        self.log_files.clear()
```

**Important:** The framework calls `cleanup()` only if it exists. Always implement it if your module uses threads, files, or network connections.

---

## Complete Minimal Example

Here's a complete working module that you can use as a template:

```python
# MyModule - A Ningu Framework Module
# Place this file in the modules/ directory

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
        
        # Main layout
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
        
        # Connect signals
        self.ui.processButton.clicked.connect(self.process_input)
        self.ui.inputLine.returnPressed.connect(self.process_input)
    
    def process_input(self):
        """Handle the process button click."""
        text = self.ui.inputLine.text()
        if text:
            self.ui.outputBox.appendPlainText(f"Processing: {text}")
            self.ui.inputLine.clear()
    
    def cleanup(self):
        """Clean up resources."""
        pass
```

---

## Module Directory Structure

For simple modules, a single `.py` file in `modules/` is sufficient. However, complex modules often have supporting directories:

```
modules/
    N_ModuleName.py                 # Main module file
    ModuleName_module_libs/         # Shared libraries (helper code)
        __init__.py                 # Optional, usually empty
        lib_helper1.py
        lib_helper2.py
    ModuleName_submodules/          # Loadable sub-modules
        enabled/                    # Active sub-modules (optional pattern)
        disabled/                   # Inactive sub-modules (optional pattern)
        submodule1.py
        submodule2.py
    ModuleName_logs/                # Output logs (if module creates logs)
        MM-DD-YYYY/                 # Date-based subdirectories
```

### Naming Conventions

| Directory | Purpose |
|-----------|---------|
| `ModuleName_module_libs/` | Shared library code imported by sub-modules |
| `ModuleName_modules/` or `ModuleName_submodules/` | Dynamically loaded sub-modules |
| `ModuleName_logs/` | Log files generated by the module |

**Examples from existing modules:**

| Module | Libraries | Sub-Modules | Logs |
|--------|-----------|-------------|------|
| Parley | `Parley_module_libs/` | `Parley_modules_client/`, `Parley_modules_server/` | `Parley_logs/` |
| SecretDecoderRing | - | `SecretDecoderRing_modules/` | - |
| AuthCheck | `AuthCheck_module_libs/` | `AuthCheck_modules/` | - |

---

## Shared Libraries (module_libs)

Shared libraries contain reusable code that sub-modules can import. This keeps sub-modules small and focused.

### Directory Location

```
modules/
    ModuleName_module_libs/
        lib_myhelper.py
        lib_another.py
```

### Adding to Python Path

Sub-modules need to add the library directory to `sys.path` before importing:

```python
# In a sub-module file
import sys
import os

# Add the module_libs directory to the path
libs_path = os.path.join(os.path.dirname(__file__), '..', 'ModuleName_module_libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

# Now import from the library
from lib_myhelper import helper_function
```

### Alternative: Main Module Adds Path

The main module can add the libs path globally during initialization:

```python
# In the main module (N_ModuleName.py)
import sys
import os

# Add module_libs to path for all sub-modules
module_libs_path = os.path.join('modules', 'ModuleName_module_libs')
if module_libs_path not in sys.path:
    sys.path.insert(0, module_libs_path)
```

### Example Library Structure

```python
# modules/ModuleName_module_libs/lib_protocol.py

def decode_message(data):
    """Decode a protocol message."""
    # Implementation
    return decoded_data

def encode_message(data):
    """Encode a protocol message."""
    # Implementation
    return encoded_data

# Constants
PROTOCOL_VERSION = "1.0"
MESSAGE_TYPES = {
    0x01: "HELLO",
    0x02: "GOODBYE",
}
```

---

## Advanced: Sub-Module Support

Some Ningu modules support loading their own sub-modules. This pattern is used by:

- **Parley** - Loads protocol decoders from `Parley_modules_client/` and `Parley_modules_server/`
- **SecretDecoderRing** - Loads encryption modules from `SecretDecoderRing_modules/`
- **AuthCheck** - Loads authentication modules from `AuthCheck_modules/`

### Sub-Module Loading Pattern

```python
import importlib.util
import os

def load_submodules(self):
    """Load sub-modules from a directory."""
    modules_dir = os.path.join('modules', 'MyModule_submodules')
    self.submodules = []
    
    if not os.path.isdir(modules_dir):
        os.makedirs(modules_dir, exist_ok=True)
        return
    
    for filename in sorted(os.listdir(modules_dir)):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(modules_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], file_path)
            
            if spec is None or spec.loader is None:
                continue
            
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                
                # Check for required function/attribute
                if hasattr(module, 'process'):
                    self.submodules.append(module)
                    
            except Exception as e:
                print(f"Error loading {filename}: {e}")
```

### Sub-Module Structure (Example: SecretDecoderRing encryption module)

```python
# SecretDecoderRing_modules/MyEncryption_v1.0.py

def decrypt(iv, key, ciphertext):
    """
    Attempt to decrypt ciphertext.
    
    Args:
        iv: Initialization vector (bytes)
        key: Encryption key (bytes)
        ciphertext: Data to decrypt (bytes)
    
    Returns:
        List of tuples: [(mode_name, plaintext_bytes), ...]
        Empty list if decryption failed.
    """
    results = []
    
    try:
        # Your decryption logic here
        plaintext = your_decrypt_function(iv, key, ciphertext)
        results.append(("ECB", plaintext))
    except Exception:
        pass
    
    return results
```

### Sub-Module Structure (Example: AuthCheck authentication module)

```python
# AuthCheck_modules/MyAuth.py

module_description = "My Custom Authentication System"

form_fields = [
    {
        'name': 'host',
        'type': 'text',
        'label': 'Host',
        'default': 'localhost'
    },
    {
        'name': 'port',
        'type': 'text',
        'label': 'Port',
        'default': '443',
        'port_toggle': 'use_tls',    # Optional: auto-change when checkbox toggled
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
        'type': 'password',          # Masked input
        'label': 'Password',
        'default': ''
    },
    {
        'name': 'use_tls',
        'type': 'checkbox',
        'label': 'Use TLS',
        'default': True
    },
    {
        'name': 'cert_file',
        'type': 'file',              # Shows file browser button
        'label': 'Certificate',
        'default': '',
        'filter': 'Certificates (*.pem *.crt);;All Files (*)'
    },
    {
        'name': 'auth_type',
        'type': 'combo',             # Dropdown
        'label': 'Auth Type',
        'default': 'Basic',
        'options': ['Basic', 'Digest', 'NTLM']
    },
    {
        'name': 'hints',
        'type': 'readonly',          # Non-editable info text
        'label': 'Hints',
        'default': 'Enter credentials and click Check'
    }
]

def authenticate(form_data):
    """
    Attempt authentication.
    
    Args:
        form_data: Dictionary of {field_name: value}
                   - text/password: str
                   - checkbox: bool
                   - combo: str (selected option)
                   - file: str (file path)
    
    Returns:
        Tuple: (success: bool, message: str)
    """
    host = form_data.get('host', '')
    username = form_data.get('username', '')
    password = form_data.get('password', '')
    use_tls = form_data.get('use_tls', False)
    
    try:
        # Your authentication logic here
        if check_credentials(host, username, password, use_tls):
            return True, f"Successfully authenticated as {username}"
        else:
            return False, "Invalid credentials"
    except Exception as e:
        return False, f"Error: {e}"
```

**AuthCheck form field types:**

| Type | Widget | Value in form_data |
|------|--------|-------------------|
| `text` | `QLineEdit` | `str` |
| `password` | `QLineEdit` (masked) | `str` |
| `checkbox` | `QCheckBox` | `bool` |
| `combo` | `QComboBox` | `str` (selected text) |
| `file` | `QLineEdit` + Browse button | `str` (file path) |
| `readonly` | `QPlainTextEdit` (disabled) | Not in form_data |

### Sub-Module Structure (Example: Parley protocol decoder)

**IMPORTANT:** The main module adds `Parley_module_libs` to `sys.path`, so sub-modules can import directly from libraries.

```python
# Parley_modules_client/Display_Client_MyProtocol.py

from datetime import datetime
from log_utils import write_to_log        # From Parley_module_libs
from lib_myprotocol import decode_proto   # Your custom library

module_description = "decode and display MyProtocol messages from client"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):
    """
    Process a message passing through the proxy.
    
    Args:
        message_num: Sequential message number for this connection (int)
        source_ip: Source IP address (str)
        source_port: Source port number (int)
        dest_ip: Destination IP address (str)
        dest_port: Destination port number (int)
        message_data: The raw message bytes (bytearray)
    
    Returns:
        message_data: The data to forward (can be modified, or return original)
    """
    # Try to decode
    decoded = decode_proto(message_data)
    
    if decoded:
        # Build output
        output = []
        output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) -------")
        output.append(decoded)
        full_output = '\n'.join(output)
        
        # Print to console AND write to connection-specific log
        print(full_output)
        write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)
    
    # Return data unchanged (or modify if this is a Modify_ module)
    return message_data
```

**Key points:**
- `module_description` attribute is displayed in the UI module list
- Use `print()` for console output
- Use `write_to_log()` from `log_utils` for connection-specific logs
- Always return `message_data` (modified or not)
- Modification modules (prefix `0-Modify_`) can alter and return different data

---

## Requirements.txt

If your module requires additional Python packages beyond PySide6, create a `requirements.txt` file in your module's directory.

### Location Options

**Option 1: Module-Specific (Recommended for Standalone Distribution)**
```
ModuleName-GUI/
    N_ModuleName.py
    requirements.txt
    README.md
    LICENSE
```

**Option 2: In the modules/ Directory**
```
modules/
    N_ModuleName.py
    ModuleName_requirements.txt
```

### Format

Standard pip requirements format with version constraints:

```
# Core GUI Framework (always required)
PySide6>=6.0.0

# Module-specific dependencies
requests>=2.28.0
cryptography>=40.0.0
```

### Best Practices

1. **Always pin minimum versions** using `>=` to ensure compatibility
2. **Comment sections** for clarity
3. **Mark optional packages** with comments
4. **Group by function** (databases, networking, etc.)

### Simple Example (SecretDecoderRing)

```
PySide6>=6.0.0
pycryptodome>=3.10.0
```

### Comprehensive Example (AuthCheck)

```
# Ningu Framework - ModuleName Module Dependencies
# ================================================
# Install with: pip install -r requirements.txt

# Core GUI Framework
PySide6>=6.0.0

# ===================
# HTTP/REST Clients
# ===================
requests>=2.28.0

# ===================
# Database Clients
# ===================
psycopg2-binary>=2.9.0     # PostgreSQL
mysql-connector-python>=8.0.0   # MySQL
redis>=4.0.0               # Redis

# ===================
# Optional (install as needed)
# ===================
# pymongo>=4.0.0           # MongoDB
# elasticsearch>=8.0.0     # Elasticsearch
```

### Installation Instructions

Include in your README:

```bash
pip install -r requirements.txt
```

Or for module-specific requirements:

```bash
pip install -r modules/ModuleName_requirements.txt
```

---

## README.md

Every module should have a README.md documenting its purpose and usage.

### Location

**Option 1: Standalone Distribution**
```
ModuleName-GUI/
    N_ModuleName.py
    README.md           # Full documentation
```

**Option 2: Within modules/ Directory**
```
modules/
    N_ModuleName.py
    README.md           # Can document Parley specifically, as shown
```

### Recommended Structure

```markdown
# ModuleName - Brief Description

**Version:** X.Y.Z  
**Author:** Your Name  
**License:** License Name  

---

## Overview

Brief description of what the module does and its primary use cases.

---

## Features

- Feature 1
- Feature 2
- Feature 3

---

## Directory Structure

```
modules/
    N_ModuleName.py
    ModuleName_module_libs/
        lib_helper.py
    ModuleName_submodules/
        submodule1.py
```

---

## Usage

1. Launch Ningu: `python ningu-v1.0.0.py`
2. Select the **ModuleName** tab
3. Step-by-step instructions...

---

## Sub-Module Development (if applicable)

Each sub-module must define:

```python
def required_function(args):
    """Description of function signature."""
    pass
```

---

## Included Sub-Modules (if applicable)

| Module | Description |
|--------|-------------|
| `SubModule1` | What it does |
| `SubModule2` | What it does |

---

## Libraries (if applicable)

| Library | Description |
|---------|-------------|
| `lib_helper.py` | What it provides |

---

## Changelog

### vX.Y.Z
- Change 1
- Change 2

### vX.Y.0
- Initial release

---

## Contact

Your Name  
Email: your@email.com
```

### Real Example (Parley README Structure)

The Parley module's README includes:
- Version, author, license header
- Overview of functionality
- Full directory structure
- Usage instructions with numbered steps
- Sub-module development API documentation
- Tables of included sub-modules organized by category
- Library descriptions
- Changelog with version history
- Contact information

---

## Existing Module Examples

| Module | File | Description |
|--------|------|-------------|
| Parley | `3_Parley.py` | TCP/TLS proxy with protocol decoding |
| SecretDecoderRing | `4_SecretDecoderRing.py` | Encryption cracker with pluggable algorithms |
| CERTcrack | `5_CERTcrack.py` | Certificate password cracker |
| AuthCheck | `5_AuthCheck.py` | Authentication system tester |

### Key Patterns from Each:

**Parley:**
- Background threading with `QThread`
- Sub-module loading from `enabled/` and `disabled/` directories
- Custom logging with connection-specific files
- Toggle buttons for TLS modes

**SecretDecoderRing:**
- Sub-module pattern for encryption algorithms
- Results displayed in `QTableWidget`
- Input format conversion (Base64, HEX, ASCII)

**CERTcrack:**
- Worker threads with signals (`QThread.Signal`)
- Progress reporting
- External tool integration (`openssl`, `keytool`)
- Multi-threading with `ThreadPoolExecutor`

**AuthCheck:**
- Dynamic form generation from sub-module metadata
- Form value persistence between module switches
- File browser integration

---

## Important Development Guidelines

### Do NOT

Based on project conventions and user preferences:

1. **Do NOT include emoji or icon characters** in output messages (no ✅, ❌, etc.)
2. **Do NOT add metadata header sections** to Python files (no `# Module:` blocks beyond the copyright header)
3. **Do NOT make changes unless explicitly asked** - if you notice issues, ask first
4. **Do NOT over-engineer** - make minimal changes to accomplish the task
5. **Do NOT "improve" working code** - even if suboptimal, leave it alone unless asked
6. **Do NOT create documentation files** unless explicitly requested

### Data Types

**Parley message_data is `bytearray`, not `bytes`:**

```python
def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):
    # message_data is bytearray - mutable!
    
    # To check content:
    if b'HTTP' in message_data:
        pass
    
    # To modify in place (for Modify_ modules):
    message_data[0:4] = b'TEST'
    
    # To convert to bytes (immutable):
    as_bytes = bytes(message_data)
    
    # To decode as string:
    try:
        as_string = message_data.decode('utf-8')
    except UnicodeDecodeError:
        as_string = message_data.decode('latin-1')  # fallback
    
    return message_data
```

### Socket and TLS Patterns (from Parley)

```python
import socket
import ssl

# TCP socket with SO_REUSEADDR (important for quick restart)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)

# TLS client connection with optional verification skip
context = ssl.create_default_context()
if not verify_certificate:
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

tls_socket = context.wrap_socket(raw_socket, server_hostname=remote_host)
```

### Threading with select()

For proxies handling multiple sockets:

```python
import select

while running:
    readable, _, _ = select.select([client_socket, server_socket], [], [], 1.0)
    
    for sock in readable:
        data = sock.recv(4096)
        if not data:
            running = False
            break
        # Process data...
```

---

## Summary Checklist

When creating a new Ningu module, ensure:

### Required
- [ ] File is placed in `modules/` directory
- [ ] Filename follows `N_ModuleName.py` pattern for ordering
- [ ] `TabContent` class exists and inherits from `QWidget`
- [ ] `__init__()` calls `super().__init__()`

### Recommended
- [ ] `TAB_LABEL` string is defined (otherwise filename is used)
- [ ] `cleanup()` method handles resource cleanup (threads, files, connections)
- [ ] Signals are connected in `__init__()` or shortly after

### For Complex Modules
- [ ] `README.md` documents usage and sub-module API
- [ ] `requirements.txt` lists dependencies with version constraints
- [ ] Shared libraries in `ModuleName_module_libs/` directory
- [ ] Sub-modules in `ModuleName_submodules/` or similar directory
- [ ] `sys.path` updated to include module_libs for sub-module imports

### For Standalone Distribution
- [ ] Module directory includes: main .py file, README.md, LICENSE, requirements.txt
- [ ] README includes: overview, features, usage, changelog, contact info

---

## Common Pitfalls and Gotchas

Things that can trip you up when writing Ningu modules:

### 1. Qt Threading Rules (CRITICAL)

**Never update UI widgets from a worker thread.** Qt is not thread-safe for UI operations.

```python
# WRONG - Will crash or behave unpredictably
class Worker(threading.Thread):
    def run(self):
        self.ui.statusBox.appendPlainText("Working...")  # BAD!

# RIGHT - Use Qt signals to communicate with the main thread
from PySide6.QtCore import QThread, Signal

class Worker(QThread):
    status_update = Signal(str)  # Define a signal
    
    def run(self):
        self.status_update.emit("Working...")  # Emit signal instead

# In TabContent:
self.worker.status_update.connect(self.ui.statusBox.appendPlainText)
```

### 2. Module Loading Happens at Startup

All modules in `modules/` are loaded when Ningu starts. If your module crashes during `__init__()`, it will:
- Print an error to the console
- Skip loading that tab
- Continue loading other modules

**Test your module's `__init__()` carefully!**

### 3. Sub-Module Paths Are Relative to CWD

When loading sub-modules, paths like `os.path.join('modules', 'MyModule_submodules')` are relative to where Ningu was launched, not where your module file is located.

```python
# This works when launched from project root:
#   python ningu-v1.0.0.py

# This breaks if launched from elsewhere:
#   cd modules && python ../ningu-v1.0.0.py
```

### 4. The enabled/disabled Pattern

Parley uses `enabled/` and `disabled/` subdirectories to let users toggle sub-modules by clicking in the UI. The click handler moves files between directories:

```python
# User clicks to disable a module:
shutil.move(
    os.path.join(enabled_dir, module_filename),
    os.path.join(disabled_dir, module_filename)
)
# Then reload the module list
```

This is a UI convenience, not a framework requirement.

### 5. cleanup() May Not Be Called on Crashes

If Ningu crashes or is killed, `cleanup()` won't run. Design accordingly:
- Use context managers for file handles when possible
- Flush logs frequently
- Don't rely on cleanup for data integrity

### 6. Module Names Must Be Valid Python Identifiers

The filename (minus `.py`) becomes the module name. Avoid:
- Spaces in filenames
- Starting with numbers (use `3_Parley.py`, not `3Parley.py`)
- Hyphens (use underscores)

### 7. Be Conservative with Code Changes

When modifying existing modules:
- Make minimal, targeted changes
- Test after each change
- Avoid "cleanup" or "optimization" unless specifically requested
- Keep backups before major refactoring

A real example: During Parley development, a well-intentioned "dead code cleanup" caused crashes. The fix was to revert and make only the essential changes.

### 8. Widget References After setupUi()

Only access UI elements after `setupUi()` has been called:

```python
class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        # WRONG - ui doesn't exist yet
        # self.ui.someButton.click()
        
        self.ui = Ui_TabContent()
        self.ui.setupUi(self)
        
        # RIGHT - now ui elements exist
        self.ui.someButton.clicked.connect(self.handler)
```

---

## Advanced Widget Patterns

### The showEvent Pattern

Override `showEvent()` to run code when the tab becomes visible (e.g., set focus):

```python
class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        # ... setup ...
    
    def showEvent(self, event):
        """Called when this tab becomes visible."""
        super().showEvent(event)
        # Set focus to a specific widget
        self.ui.inputLine.setFocus()
```

### Persisting State Between Sessions

For simple state persistence, use a JSON file:

```python
import json
import os

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = os.path.join('modules', 'MyModule_config.json')
        self.load_config()
    
    def load_config(self):
        """Load saved configuration."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.ui.inputLine.setText(config.get('last_input', ''))
            except Exception:
                pass
    
    def save_config(self):
        """Save current configuration."""
        config = {
            'last_input': self.ui.inputLine.text()
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
    
    def cleanup(self):
        """Called when Ningu closes."""
        self.save_config()
```

### Disabling Widgets During Operations

```python
def start_operation(self):
    # Disable all input widgets
    self.ui.inputLine.setEnabled(False)
    self.ui.startButton.setEnabled(False)
    self.ui.stopButton.setEnabled(True)
    
def finish_operation(self):
    # Re-enable widgets
    self.ui.inputLine.setEnabled(True)
    self.ui.startButton.setEnabled(True)
    self.ui.stopButton.setEnabled(False)
```

### Error Handling Best Practices

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
        # Log the full error for debugging, but show user-friendly message
        import traceback
        print(f"Unexpected error: {traceback.format_exc()}")
        self.ui.statusBox.appendPlainText(f"Error: {e}")
```

---

## Qt/PySide6 Essentials

Key Qt concepts for Ningu module development:

### Signals and Slots

Qt's event system. Signals are emitted, slots receive them:

```python
# Connect a button click to a method
self.ui.myButton.clicked.connect(self.on_button_clicked)

# Connect with a lambda for parameters
self.ui.myButton.clicked.connect(lambda: self.do_something("param"))
```

### Common Signal Patterns

| Widget | Common Signals |
|--------|---------------|
| `QPushButton` | `clicked`, `pressed`, `released` |
| `QLineEdit` | `textChanged`, `returnPressed`, `editingFinished` |
| `QComboBox` | `currentIndexChanged`, `currentTextChanged` |
| `QCheckBox` | `stateChanged`, `toggled` |
| `QListWidget` | `itemClicked`, `itemSelectionChanged`, `currentItemChanged` |
| `QTableWidget` | `cellClicked`, `itemSelectionChanged` |
| `QPlainTextEdit` | `textChanged` |

### QThread for Background Work

```python
from PySide6.QtCore import QThread, Signal

class MyWorker(QThread):
    progress = Signal(int)      # Emits progress percentage
    result = Signal(dict)       # Emits result data
    error = Signal(str)         # Emits error message
    finished_work = Signal()    # Emits when done
    
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

### Checkable Buttons (Toggles)

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

## Debugging Tips

### Where Errors Appear

1. **Console/Terminal** - Module loading errors, uncaught exceptions
2. **StatusTextBox** - Module-specific status messages (if you write them there)
3. **Qt's internal output** - Some Qt warnings go to stderr

### Common Error Messages

| Error | Likely Cause |
|-------|--------------|
| `Error: module 'X' lacks a 'TabContent' class` | Missing or misspelled `TabContent` class |
| `Error loading 'X': ...` | Exception during module import or `__init__` |
| `'TabContent' in 'X' is not a QWidget` | `TabContent` doesn't inherit from `QWidget` |
| `AttributeError: 'Ui_TabContent' has no attribute 'X'` | Referencing UI element before `setupUi()` is called |
| `RuntimeError: wrapped C/C++ object has been deleted` | Accessing widget after it was destroyed |

### Testing a Module Standalone

You can test your module without the full framework:

```python
# test_mymodule.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# Import your module
from modules.N_MyModule import TabContent

app = QApplication(sys.argv)
window = QMainWindow()
widget = TabContent()
window.setCentralWidget(widget)
window.show()
app.exec()
```

### Print Debugging

In PySide6, `print()` statements go to the console. For the UI, use your status box:

```python
# Console only
print("Debug: something happened")

# UI status box (if you have one)
self.ui.StatusTextBox.appendPlainText("Debug: something happened")
```

---

## Cross-Platform Development

Ningu modules should work on Windows, macOS, and Linux. Follow these practices:

### Path Handling

**Always use `os.path.join()` or `pathlib.Path`** - never hardcode slashes:

```python
# WRONG - breaks on Windows
path = "modules/MyModule_libs/helper.py"

# RIGHT - works everywhere
path = os.path.join("modules", "MyModule_libs", "helper.py")

# ALSO RIGHT - pathlib is even better
from pathlib import Path
path = Path("modules") / "MyModule_libs" / "helper.py"
```

### File Operations

```python
# Get user's home directory
from pathlib import Path
home = Path.home()  # Works on all platforms

# Get temp directory
import tempfile
temp_dir = tempfile.gettempdir()

# Check if file exists (case-sensitive on Linux, not on Windows/macOS)
if os.path.exists(filepath):
    pass
```

### External Tool Availability

Check if tools exist before using them:

```python
import shutil

# Check if a tool is available
if shutil.which("openssl") is None:
    self.ui.statusBox.appendPlainText("ERROR: openssl not found in PATH")
    return

# Run external commands
import subprocess
result = subprocess.run(
    ["openssl", "version"],
    capture_output=True,
    text=True,
    timeout=10  # Always set a timeout
)
```

### Line Endings

When writing text files, be explicit about line endings if it matters:

```python
# Let Python handle it (uses OS default)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Force Unix line endings (LF) - recommended for logs
with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
```

### Encoding

**Always specify encoding** when opening text files:

```python
# WRONG - uses system default (varies by OS)
with open(filepath, 'r') as f:
    content = f.read()

# RIGHT - explicit UTF-8
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
```

### Process Execution

```python
import subprocess
import sys

# Run Python scripts portably
subprocess.run([sys.executable, "script.py"])

# Hide console window on Windows (for GUI apps)
startupinfo = None
if sys.platform == "win32":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

result = subprocess.run(
    ["some_command"],
    capture_output=True,
    startupinfo=startupinfo
)
```

### Platform-Specific Code (When Unavoidable)

```python
import sys

if sys.platform == "win32":
    # Windows-specific code
    config_dir = os.path.join(os.environ.get("APPDATA", ""), "MyModule")
elif sys.platform == "darwin":
    # macOS-specific code
    config_dir = os.path.expanduser("~/Library/Application Support/MyModule")
else:
    # Linux/Unix
    config_dir = os.path.expanduser("~/.config/mymodule")
```

### Things to Avoid

| Avoid | Use Instead |
|-------|-------------|
| Hardcoded `/` or `\` in paths | `os.path.join()` or `Path()` |
| `os.system()` | `subprocess.run()` |
| Assuming case sensitivity | Be consistent, prefer lowercase |
| Assuming tool availability | Check with `shutil.which()` |
| Bare `open()` without encoding | `open(f, encoding='utf-8')` |
| `~` in paths | `os.path.expanduser("~")` |
| Hardcoded temp paths | `tempfile.gettempdir()` |

---

## Code Style Conventions

Existing Ningu modules follow these patterns:

### File Header

```python
# ModuleName - part of the Ningu Framework
# Copyright (C) 2025 Your Name - your@email.com
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
```

### Version at Top

```python
VERSION = "1.0.0"
TAB_LABEL = f"ModuleName v{VERSION}"
```

### Class Order

1. Helper classes (workers, utilities)
2. `Ui_TabContent` class
3. `TabContent` class

### Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Module file | `N_ModuleName.py` | `3_Parley.py` |
| Sub-module dir | `ModuleName_submodules/` | `Parley_modules_client/` |
| Library dir | `ModuleName_module_libs/` | `Parley_module_libs/` |
| Library file | `lib_name.py` | `lib_jwt.py` |
| Sub-module file | `Purpose_Direction_Protocol.py` | `Display_Client_FIX.py` |
| Cred extraction | `Creds_Client_Protocol.py` | `Creds_Client_HTTP_Basic.py` |

### Semantic Versioning

Use `MAJOR.MINOR.PATCH`:
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

---

## Integrating Standalone Modules

To add a standalone module (like `CERTcrack-GUI/`) to your Ningu installation:

### Step 1: Copy the Main Module File

```bash
cp CERTcrack-GUI/5_CERTcrack.py modules/
```

### Step 2: Copy Supporting Directories (if any)

```bash
cp -r CERTcrack-GUI/CERTcrack_module_libs modules/
cp -r CERTcrack-GUI/CERTcrack_modules modules/
```

### Step 3: Install Dependencies

```bash
pip install -r CERTcrack-GUI/requirements.txt
```

### Step 4: Launch Ningu

```bash
python ningu-v1.0.0.py
```

The module should appear as a new tab.

---

## Template: Complete Module with Worker Thread

A production-ready template combining all patterns:

```python
# N_MyModule.py - A Ningu Framework Module
# Copyright (C) 2025 Your Name - your@email.com
# License: GPL v3

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QPlainTextEdit, QFrame,
    QProgressBar, QSpacerItem, QSizePolicy
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
        self.startButton.setFont(QFont())
        self.startButton.font().setBold(True)
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
        
        # Connect signals
        self.ui.startButton.clicked.connect(self.start_work)
        self.ui.stopButton.clicked.connect(self.stop_work)
        self.ui.inputLine.returnPressed.connect(self.start_work)
    
    def start_work(self):
        text = self.ui.inputLine.text().strip()
        if not text:
            self.ui.outputBox.appendPlainText("Please enter input")
            return
        
        # Disable start, enable stop
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.ui.progressBar.setVisible(True)
        
        # Create and start worker
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
        """Called when Ningu closes."""
        if self.worker:
            self.worker.stop()
            self.worker.wait(5000)  # Wait up to 5 seconds
```

---

## Framework Source Reference

The Ningu framework source (`ningu-v1.0.0.py`) shows exactly how modules are loaded:

```python
def load_modules(self) -> None:
    module_dir = "modules"
    os.makedirs(module_dir, exist_ok=True)

    for fname in sorted(
        f for f in os.listdir(module_dir)
        if f.endswith(".py") and f != "__init__.py"
    ):
        path = os.path.join(module_dir, fname)
        spec = importlib.util.spec_from_file_location(fname[:-3], path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, "TabContent"):
            widget = module.TabContent()
            if isinstance(widget, QWidget):
                tab_label = getattr(module, "TAB_LABEL", fname[:-3])
                self.tabs.addTab(widget, tab_label)
                self.widgets.append(widget)
```

The `closeEvent` handler calls `cleanup()` on each widget:

```python
def closeEvent(self, event):
    for widget in self.widgets:
        if hasattr(widget, 'cleanup'):
            widget.cleanup()
    event.accept()
```

---

## Quick Reference

### Minimum Viable Module (Copy-Paste Ready)

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

TAB_LABEL = "MyModule"

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Hello World"))
```

### Required Exports

| Export | Required | Type | Purpose |
|--------|----------|------|---------|
| `TabContent` | YES | Class (QWidget) | The widget shown in the tab |
| `TAB_LABEL` | No | str | Tab display name (default: filename) |

### Sub-Module Required Exports by Parent

| Parent Module | Required Export | Signature |
|---------------|-----------------|-----------|
| **SecretDecoderRing** | `decrypt` | `decrypt(iv, key, ciphertext) -> [(mode, plaintext), ...]` |
| **AuthCheck** | `authenticate` | `authenticate(form_data) -> (success, message)` |
| **AuthCheck** | `form_fields` | List of field dicts |
| **AuthCheck** | `module_description` | str |
| **Parley** | `module_function` | `module_function(msg_num, src_ip, src_port, dst_ip, dst_port, data) -> data` |
| **Parley** | `module_description` | str |

### Common Import Block

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QPlainTextEdit,
    QFrame, QTableWidget, QTableWidgetItem, QListWidget,
    QComboBox, QCheckBox, QProgressBar, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal
```

---

## Lessons Learned (Real Development Examples)

These are actual lessons from developing Ningu modules:

### 1. Test Incrementally

When adding features to Parley (TLS verification bypass), the approach that worked:
1. Make ONE change
2. Test it works
3. Commit/backup
4. Repeat

The approach that failed:
1. Make multiple "improvements" at once
2. Application crashes
3. Hard to identify which change broke it

### 2. Dead Code Removal is Risky

Attempted to remove "dead code" from Parley including:
- Unused imports
- Empty frames
- Redundant comments

Result: Application crashed. Some "dead" code was actually referenced.

**Lesson:** Only remove code you fully understand. When in doubt, leave it.

### 3. Verify API Signatures by Reading Actual Code

Initial documentation for Parley sub-modules was wrong:
- Documented: `module_function(data, connection_info, log_func)`
- Actual: `module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data)`

**Lesson:** Always verify APIs by reading existing working modules, not by guessing.

### 4. Backups Before Major Changes

Workflow that prevented disasters:
1. Create versioned backup: `v1.2.0/`
2. Make changes
3. Test
4. If broken, restore from backup

### 5. The User Knows the Codebase

When the user says "maybe it is AuthCheck-GUI?" after "AuthCheck" fails - they're usually right. Trust their knowledge of their own repositories and naming conventions.

---

## Document Version

This guide was written for Ningu Framework v1.0.0 and tested with:
- Parley v1.2.0
- SecretDecoderRing v1.3.4
- CERTcrack v1.3.0
- AuthCheck v1.0.0

Last updated: January 2026
