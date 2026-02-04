# Ningu Sub-Module Development

This reference covers creating sub-modules for Parley, SecretDecoderRing, and AuthCheck.

---

## Parley Sub-Modules

Parley loads protocol decoders from `Parley_modules_client/` and `Parley_modules_server/`.

### Required Exports

```python
module_description = "decode and display MyProtocol messages from client"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):
    """
    Process a message passing through the proxy.
    
    Args:
        message_num: Sequential message number (int)
        source_ip: Source IP address (str)
        source_port: Source port number (int)
        dest_ip: Destination IP address (str)
        dest_port: Destination port number (int)
        message_data: Raw message bytes (bytearray - MUTABLE!)
    
    Returns:
        message_data: The data to forward (can be modified)
    """
    # Your decoding logic here
    return message_data
```

### Key Points

- `message_data` is `bytearray`, not `bytes` - it's mutable
- Always return `message_data` (modified or not)
- Use `print()` for console output
- Use `write_to_log()` from `log_utils` for connection logs
- Modification modules (prefix `0-Modify_`) can alter the data

### Example: Protocol Decoder

```python
from datetime import datetime
from log_utils import write_to_log  # From Parley_module_libs

module_description = "decode and display MyProtocol messages"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):
    # Check if this is our protocol
    if b'MYPROTO' not in message_data:
        return message_data
    
    # Decode and display
    output = f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] Message #{message_num}"
    print(output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, output)
    
    return message_data
```

### Naming Conventions

| Prefix | Purpose |
|--------|---------|
| `Display_Client_` | Display client-to-server messages |
| `Display_Server_` | Display server-to-client messages |
| `0-Modify_Client_` | Modify client-to-server messages |
| `0-Modify_Server_` | Modify server-to-client messages |
| `Creds_Client_` | Extract credentials from client messages |

---

## SecretDecoderRing Sub-Modules

SecretDecoderRing loads encryption modules from `SecretDecoderRing_modules/`.

### Required Export

```python
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
        # Your decryption logic
        plaintext = your_decrypt_function(iv, key, ciphertext)
        results.append(("ECB", plaintext))
    except Exception:
        pass
    
    return results
```

### Example: Custom Encryption Module

```python
# SecretDecoderRing_modules/MyEncryption_v1.0.py

from Crypto.Cipher import AES

def decrypt(iv, key, ciphertext):
    results = []
    
    # Try ECB mode (no IV)
    try:
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        results.append(("AES-ECB", plaintext))
    except Exception:
        pass
    
    # Try CBC mode
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        results.append(("AES-CBC", plaintext))
    except Exception:
        pass
    
    return results
```

---

## AuthCheck Sub-Modules

AuthCheck loads authentication modules from `AuthCheck_modules/`.

### Required Exports

```python
module_description = "My Custom Authentication System"

form_fields = [
    {
        'name': 'host',
        'type': 'text',
        'label': 'Host',
        'default': 'localhost'
    },
    {
        'name': 'username',
        'type': 'text',
        'label': 'Username',
        'default': ''
    },
    {
        'name': 'password',
        'type': 'password',  # Masked input
        'label': 'Password',
        'default': ''
    },
    {
        'name': 'use_tls',
        'type': 'checkbox',
        'label': 'Use TLS',
        'default': True
    }
]

def authenticate(form_data):
    """
    Attempt authentication.
    
    Args:
        form_data: Dictionary of {field_name: value}
    
    Returns:
        Tuple: (success: bool, message: str)
    """
    host = form_data.get('host', '')
    username = form_data.get('username', '')
    password = form_data.get('password', '')
    
    try:
        if check_credentials(host, username, password):
            return True, f"Successfully authenticated as {username}"
        else:
            return False, "Invalid credentials"
    except Exception as e:
        return False, f"Error: {e}"
```

### Form Field Types

| Type | Widget | Value in form_data |
|------|--------|-------------------|
| `text` | QLineEdit | str |
| `password` | QLineEdit (masked) | str |
| `checkbox` | QCheckBox | bool |
| `combo` | QComboBox | str (selected text) |
| `file` | QLineEdit + Browse | str (file path) |
| `readonly` | QPlainTextEdit (disabled) | Not included |

### Advanced Field Options

```python
{
    'name': 'port',
    'type': 'text',
    'label': 'Port',
    'default': '443',
    'port_toggle': 'use_tls',  # Auto-change when checkbox toggled
    'tls_port': '443',
    'non_tls_port': '80'
},
{
    'name': 'cert_file',
    'type': 'file',
    'label': 'Certificate',
    'default': '',
    'filter': 'Certificates (*.pem *.crt);;All Files (*)'
},
{
    'name': 'auth_type',
    'type': 'combo',
    'label': 'Auth Type',
    'default': 'Basic',
    'options': ['Basic', 'Digest', 'NTLM']
}
```

---

## Shared Libraries (module_libs)

Sub-modules can import from shared libraries:

```python
# In sub-module
import sys
import os

libs_path = os.path.join(os.path.dirname(__file__), '..', 'ModuleName_module_libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

from lib_myhelper import helper_function
```

**Note:** Parley adds its `module_libs` to `sys.path` automatically, so Parley sub-modules can import directly.
