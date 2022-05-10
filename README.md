
# 430L - Final Project

API for Saref El Yom website and desktop application.




## Authors

- [@leakhairallah](https://www.github.com/leakhairallah)



## How to run

- You'll find a file db_config.py, open and modify the url in the following format
```http
  mysql+pymysql://<mysql_username>:<mysql_password>@<mysql_host>:<mysql_port>/<mysql_db_name>
```
- Proceed by installing the requirements with the following command
```http
    pip install -r requirements.txt
```
- After changing the url to your database, in the main project directory run the following commands from python
```http
	from app import db
	db.create_all()
	exit()
		
```
- Finally make your way to the main project directory and run the following command
```http
    flask run
```


## API Reference

## Models

### User:
- id *int* **PK**
- balance_lbp *float* default: 0
- balance_usd *float* default: 0
- user_name *string(30)*
- hashed_password *string(120)*
- is_admin *boolean*

### Transaction:
- id *int* **PK**
- usd_amount *float*
- lbp_amount *float*
- added_date *date*
- user_id *int* **FK references User.id**

### Item:
- id *int* **PK**
- usdAmount *float*
- lbpAmount *float*
- sell *boolean*
- bought *int* **FK references User.id**
- user_id *string(30)* **FK references User.user_name**

## Paths


#### Get exchange Rates

```http
  GET /exchangeRate
```
Description: returns exchange rates with the transactions made within the last 3 days

#### Get statistics

```http
  GET /stats
```

Description: returns average of exchange rates per day, and count of transaction per day, within the last 20 days

#### Get items

```http
  GET /getItems
```

Description: returns all items that were not bought

#### Get items by user

```http
  GET /getItemsByUser
```

Description: returns the items that were either bought or put up by the user that made the request

#### Get statistics

```http
  GET /transaction
```

Description: returns transactions that were made by the user that made the request

#### Get user info

```http
  GET /userInfo
```

Description: returns the fields of the user that made the request

#### Post add item

```http
  POST /addItem
```

Description: adds an item to the databae with the ID of the usr that put it up

#### Post purchase

```http
    POST /purchase
```

Description: adjust balances of the 2 users that were included in the item purchase

#### Post sign up

```http
  POST /signUp
```

Description: adds a user and its hashed password to the database

#### Post authentication

```http
  POST /authentication
```

Description: authenticates the user with the username and password provided and generates a token


#### Post add money

```http
  GET /addMoney
```

Description: available only to admin, admin adds money into the user's balances (username is requested)

#### Post transaction

```http
  POST /transaction
```

Description: returns the transactions made by the user that made the request

## Functions

#### create_token(user_id)

Generates a token with the user_id provided

#### extract_atuh_token(authenticated_request)

Extracts the token from the request

#### decode_token(token)

Decodes the token extracted

#### getRates()

Computes the rates


## Documentation

Documentation
```
exchange-backend/430L_prohect/saref-el-yom-api-specifiation
```

