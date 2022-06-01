# install gunicorn flask
pip3 install gunicorn flask

# run kline service in dev
``` shell
cd kline
flask run --port 8080
```

# run code service in dev
``` shell
cd code
flask run --port 8080
```

# run kline service in product
``` shell
cd kline
gunicorn --bind 0.0.0.0:8080 wsgi:app
```