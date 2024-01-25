# FortiCare python SDK

## Prerequisites

- A FortiCare account
- [An API User must be created through IAM portal](https://docs.fortinet.com/document/forticloud/latest/identity-access-management-iam/282341/adding-an-api-user)

## Installation

```bash
git clone --depth=1 https://github.com/cprevot93/forticare.git
cd forticare
pip install -r requirements.txt
pip install .
```

## Usage

```python
from FortiCare import forticare

API_USERNAME="<your_username>" # or os.environ.get('API_USERNAME')
API_PASSWORD="<your_password>" # or os.environ.get('API_PASSWORD')

ff = FortiCare(API_USERNAME, API_PASSWORD, auto_login=False, timeout=20, debug=False)
ff.login() # optional is auto_login is set to True
ff.get_products()
```

## Features

- Auto login: login automatically when the token is None or expired
- Debug: print the request and response with logging module and logger name `forticare`
- All FortiCare API endpoints are available
- Python objects for easy manipulation: [Asset](https://github.com/cprevot93/forticare/blob/28a090c1945ba7eff9604b65cc8d7acd8a8c2601/forticare/asset.py#L194C7-L194C12), Contract, Product, Service, License, etc.
- Error handling according to FortiCare documentation
- Documentation with docstrings and type hints

## Tests

Create a `env.py` file with the following content:

```python
API_USERNAME=your_username
API_PASSWORD=your_password
```

Then run the tests:

```bash
make tests
# OR
pytest tests
```

## Authors

Charles PREVOT @ [QUIB-IT](https://www.quib-it.com) | 2023-2024
