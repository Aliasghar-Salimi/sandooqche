
# sandooqche - A Django Accounting System

MyMoney is a web-based accounting system built with Django that allows users to track their expenses and incomes. It provides features to:

 - Submit new expenses and incomes
 - View a list of all past transactions
 - Calculate the total sum of expenses and incomes
This project utilizes cURL commands to interact with the API endpoints exposed by the Django application.

## Getting Started

#### Prerequisites:

 - Python 3.x
 - pip (package installer for Python)

#### Installation:

- *1- Clone this repository:*
    
        git clone https://github.com/Aliasghar-Salimi/sandooqche.git

- *2- Create a virtual environment:*

        python3 -m venv venv

      source venv/bin/activate  # Linux/macOS
      venv\Scripts\activate.bat  # Windows

- *3- Install dependencies:*

        pip install -r requirements.txt

#### Running the application:

- *1- Migrate the database schema:*

        python manage.py migrate

 - *2- Run the development server:*

        python manage.py runserver
This will start the development server on http://localhost:8000/ by default.


## API Reference

#### submit (add) an expense

```http
  POST /submit/expense/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `date`    |          |**optional**                |
| `text`    | `string` |                            |
| `amount`  | `integer`|                            |
| `token`   |          | Required


#### submit (add) an income

```http
  POST /submit/income/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `date`    |          |**optional**                |
| `text`    | `string` |                            |
| `amount`  | `integer`|                            |
| `token`   |          | **Required**



#### retrieve username

```http
  POST /whoami/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token`   |          | **Required** |


#### get expenses

```http
  POST /query/expenses/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token`   |          | **Required** |
| `num`     | `integer`| **optional**|



#### get incomes

```http
  POST /query/incomes/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token`   |          | **Required**         |
| `num`     | `integer`| **optional**|


#### General Status of a user as Json (income,expense)

```http
  POST /generalstat/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token`   |          | **Required**               |




#### edit an expense

```http
  POST /edit/expense/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token`   |          | **Required**               |
| `id`      | `integer`| **Required**               |
| `text`    | `string` | optional                   |
| `amount`  | `integer`| optional                   |


#### edit an income

```http
  POST /edit/income/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token`   |          | **Required**               |
| `id`      | `integer`| **Required**               |
| `text`    | `string` | optional                   |
| `amount`  | `integer`| optional                   |

