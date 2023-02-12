## Introduction

This application is used to create or ask for reviews about books or articles.

It contains the following features:
- authentification system with username and password.
- following users to see the reviews they created or asked for.
- seeing which users are following you.
- creation, update or deletion of your own reviews or tickets (when you ask for a review)
- seeing every content from you or the one you follow in the main flow page.
- seeing the content you created in the my-posts page.

This applications come with a database example with a few users, tickets and reviews created to quickly show you how it can work.

## Prerequisites

You must have Python 3.6 or higher installed in order to execute this code.

## Installation

1 - Clone the github Repository.

```bash
git clone https://github.com/HaroldHaldemann/DjangoApp
```

2 - Create your virtual environment.

```bash
python -m venv name-virtual-env
```

3 - Activate your virtual environment.

On Windows
```windows
name-virtual-env\Scripts\activate.bat #In cmd
name-virtual-env\Scripts\Activate.ps1 #In Powershell
```

NB: If you activate your environment with Powershell, don't forget to enable running script :
```windows
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

On Unix/MacOs
```bash
source name-virtual-env/bin/activate
```

4 - Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required modules.

```bash
pip install -r ./requirements.txt
```

## Usage

To execute this application, go to the djangoapp folder:

```bash
cd ./djangoapp
```

Then execute the following command to launch the local server:

```python
python ./manage.py runserver
```

The server will be available at http://127.0.0.1:8000/
