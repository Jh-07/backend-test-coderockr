# Backend Challenge Project for Coderockr

---
## Description
This project is simulating an investment manager, it can create users (investment owners) and investments using the endpoints.
I created this for practicing purposes using django rest framework
---
## Features

- _CRUD_ endpoint for "Owners"
- _CRUD_ endpoint for "Investments"
- _Withdraw_ PUT endpoint
    - It can be used in two ways, passing the investment Id:
      1. using a body with _withdraw_date_ in format "YYYY-MM-DD". This sets an especific date of withdrawal
      2. No body, in this case _withdraw_date_ is set to today
- Unitests for each flow located at test_models file in tests folder
- Dynamic fields such as balance, tax and gains of a investment


## How to run

Clone this repo, create a venv and install the dependencies used in requirements.txt
```python
pip install -r requirements.txt
```
After that create a superuser (This api doesn't have authentication [yet])
```python
python manage.py createsuperuser
```
Then makemigrations and migrate the SQL database
```python
python manage.py makemigrations
#Then
python manage.py migrate
```
Run at localhost
```python
python manage.py runserver
```
### Endpoints
```python
/owners # -> Lists all owners
/owners/<id> # -> Refers to a especific owner by id
/investments # -> Lists all investments. 
             # If investment is already withdrawn, shows net gains, aplied taxes, and total gains without taxes
/investments/<id> # -> Refers to a especific investment by id
/investments/?owners_name=<owner name> # -> Partial search investmets by owner's names
/investments/?expected_date=<yyyy-mm-dd> # -> Lists all investments not withdrawn and shows expected balance for the provided date
/investments/<id>/withdraw # -> PUT endpoint, if no body is sent, withdraw date is today
```
---

## Extra business rules

These were optional for the challenge, but it felt wrong without them
and made a little safer and realistic


### Added rules

#### Owners
1. Owner name can't be lesser than 3 characters or more than 100, and can't have symbols nor numbers
2. Owner has to be 13 years old or higher

#### Investments
1. Investments have owners
2. Withdraw date cant be in the future (tomorrow or after)
---
## Tests
A made unitests for every data flow, you can look at it them at /tests folder
To run it, use command:
```python
 python manage.py test investment_manager.tests.test_models
 ```

Made by Jh07