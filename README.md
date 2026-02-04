# Ningu (忍具) Framework

**Author:** Garland Glessner  
**License:** [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)

---

## 🧩 Overview

**Ningu (忍具)** is a modular, plugin-based GUI framework written in Python using PySide6.  
The name "Ningu" (忍具) refers to "ninja tools" in Japanese, and this framework is designed to load and display self-contained GUI components dynamically as separate tabs.

It is ideal for creating toolkits, hacking suites, or internal developer dashboards where functionality is organized in a modular fashion.

---

## 🚀 Features

- 🧱 Modular architecture — just drop `.py` files in the `modules/` directory.
- 🖥️ Dynamic tab-loading based on plugin contents.
- 🎛️ Tabs aligned to the left for a clean UX.
- ✅ Automatic resource cleanup on close (`cleanup()` method support).
- 📛 Extracts program name and version from the script filename (e.g. `ningu-v1.0.0.py`).

---

## 📁 Directory Structure

```

ningu-v1.0.py
modules/

````

---

## 🔧 Usage

### ✅ Requirements

- Python 3.7+
- [PySide6](https://pypi.org/project/PySide6/)

```bash
pip install PySide6
````

### ▶️ Run the App

```bash
python ningu-v1.0.0.py
```

The program will:

1. Load all `.py` files in the `modules/` directory.
2. Expect each module to define a `TabContent` class (subclass of `QWidget`).
3. Display each module in its own tab.

---

## 📦 Module Development

Each module must be a `.py` file inside the `modules/` directory and should export a `TabContent` class.

### Example:

```python
# modules/hello.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

TAB_LABEL = "Hello"

class TabContent(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Hello from a module!"))
        self.setLayout(layout)

    def cleanup(self):
        print("Cleaning up Hello module")
```

---

## 🤖 AI-Assisted Development

This repository includes resources for AI-assisted module development.

### Cursor IDE

If you're using [Cursor](https://cursor.com/), the included AI skill at `.cursor/skills/ningu-framework/` is automatically discovered. Simply ask your AI assistant to help with Ningu module development, and it will use the skill to provide context-aware guidance.

Example prompts:
- "Create a new Ningu module for..."
- "How do I add a Parley sub-module?"
- "Help me implement a worker thread in my module"

### Microsoft Visual Studio Code

For VS Code users with Claude or other AI assistants, reference the comprehensive documentation directly:

1. Open `NINGU_MODULE_DEVELOPMENT.md` in your editor
2. Ask your AI assistant to read it: *"Read NINGU_MODULE_DEVELOPMENT.md and use it as a reference for helping me develop Ningu modules"*
3. The AI will use the documentation to provide accurate guidance on module structure, sub-module APIs, Qt patterns, and more

The `NINGU_MODULE_DEVELOPMENT.md` file contains complete documentation including:
- Module structure and requirements
- Sub-module development for Parley, SecretDecoderRing, and AuthCheck
- Qt/PySide6 widget patterns and threading
- Cross-platform development best practices
- Complete code templates

---

## 🧼 Graceful Shutdown

* Pressing Ctrl-C from the terminal triggers a clean exit.
* If a module defines a `.cleanup()` method, it will be invoked on shutdown.

---

## 📜 License

This project is licensed under the **GNU GPL v3.0** — see [LICENSE](https://www.gnu.org/licenses/gpl-3.0.html) for details.

---

## ✉️ Contact

Garland Glessner
📧 [gglessner@gmail.com](mailto:gglessner@gmail.com)
