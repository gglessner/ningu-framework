---
name: ningu-framework
description: Develop modules for the Ningu Framework, a PySide6 plugin-based GUI toolkit. Use when creating Ningu modules, TabContent classes, sub-modules for Parley/SecretDecoderRing/AuthCheck, or asking about Ningu module structure, cleanup methods, or Qt threading patterns.
---

# Ningu Framework Module Development

This skill helps you create modules for the Ningu Framework - a PySide6-based GUI framework that dynamically loads Python modules as tabs.

## Quick Start

Every Ningu module requires:

1. **File location**: `modules/N_ModuleName.py` (N controls tab order)
2. **TabContent class**: Inherits from `QWidget`
3. **TAB_LABEL** (optional): String for tab display name

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

TAB_LABEL = "MyModule v1.0.0"

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Hello from MyModule!"))
    
    def cleanup(self):
        """Called when Ningu closes - stop threads, close files."""
        pass
```

## Module Structure Patterns

### Simple Module
Single `.py` file in `modules/` directory.

### Complex Module with Sub-Modules
```
modules/
    N_ModuleName.py              # Main module
    ModuleName_module_libs/      # Shared library code
        lib_helper.py
    ModuleName_submodules/       # Dynamically loaded sub-modules
        submodule1.py
    ModuleName_logs/             # Output logs (if needed)
```

## Critical Rules

### Qt Threading (CRITICAL)
**Never update UI from worker threads.** Use Qt signals:

```python
from PySide6.QtCore import QThread, Signal

class Worker(QThread):
    status_update = Signal(str)  # Define signal
    
    def run(self):
        self.status_update.emit("Working...")  # Emit, don't touch UI

# In TabContent:
self.worker.status_update.connect(self.ui.statusBox.appendPlainText)
```

### The cleanup() Method
Always implement if using threads, files, or connections:

```python
def cleanup(self):
    if self.worker_thread:
        self.worker_thread.stop()
        self.worker_thread.wait()
    for f in self.open_files.values():
        f.close()
```

### Data Types
- Parley `message_data` is `bytearray` (mutable), not `bytes`
- Always return `message_data` from Parley module_function

## Development Guidelines

### Do NOT
- Include emoji in output messages
- Add metadata headers beyond copyright
- Make changes unless explicitly asked
- Over-engineer or "improve" working code
- Create documentation files unless requested

### Do
- Use `os.path.join()` for paths (cross-platform)
- Specify `encoding='utf-8'` when opening files
- Test incrementally - one change at a time
- Implement `cleanup()` for any resources

## Tab Ordering

Tabs appear alphabetically. Use numeric prefixes:

| Filename | Position |
|----------|----------|
| `1_First.py` | 1st |
| `2_Second.py` | 2nd |
| `ZZ_Last.py` | Last |

## Common Widgets

| Widget | Purpose |
|--------|---------|
| `QPlainTextEdit` | Multi-line text (use `setReadOnly(True)` for output) |
| `QLineEdit` | Single-line input |
| `QPushButton` | Buttons (use `setCheckable(True)` for toggles) |
| `QTableWidget` | Results tables |
| `QComboBox` | Dropdowns |

## Sub-Module Development

For creating sub-modules for existing Ningu modules, see [submodules.md](submodules.md):
- **Parley**: Protocol decoders with `module_function()`
- **SecretDecoderRing**: Encryption with `decrypt()`
- **AuthCheck**: Authentication with `authenticate()` and `form_fields`

## Additional Resources

- [reference.md](reference.md) - Complete API reference and widget patterns
- [submodules.md](submodules.md) - Sub-module development for Parley/SecretDecoderRing/AuthCheck
- [examples.md](examples.md) - Full module templates with worker threads

## Quick Reference

| Export | Required | Type | Purpose |
|--------|----------|------|---------|
| `TabContent` | YES | Class (QWidget) | Widget shown in tab |
| `TAB_LABEL` | No | str | Tab name (default: filename) |
| `cleanup()` | No | Method | Resource cleanup on close |

### Common Import Block

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QPlainTextEdit, QFrame,
    QTableWidget, QComboBox, QCheckBox, QProgressBar
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal
```
