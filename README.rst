FortiCare python SDK
==================

# Installation

```bash
pip install -r requirements.txt
```
# FortiCare Credentials
[Documentation]()

# Usage

```python
from FortiCare import forticare

ff = FortiCare(API_USERNAME, API_PASSWORD)
ff.login()

```

# Installation

```bash
pip install .
```

# Tests

Create a `env.py` file with the following content:

```python
API_USERNAME=your_username
API_PASSWORD=your_password
PROGRAM_SN=your_program_sn
```

Then run the tests:

```bash
pytest tests
```

# Authors
Charles PREVOT | 2023
