# what for

this project is tools for trading stocks.

## agu

- get listed stocks code
- get daily kline data within 3 years
- send email msg
- get top N net inflow code
- get trade info of code
- get operate_dept buy symbol name

## install gunicorn flask

pip3 install gunicorn flask cachetools

## run kline service in dev

``` shell
cd kline
flask run --port 8080
```

## run code service in dev

``` shell
cd code
flask run --port 8080
```

## run kline service in product

``` shell
cd kline
gunicorn --bind 0.0.0.0:8080 wsgi:app
```
