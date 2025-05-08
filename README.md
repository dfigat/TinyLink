# TinyLink
TinyLink is a simple URL shortener service using Django and Django Rest Framework.
It allows generating short (tiny) links to manage long URLs efficiently
(in development)


## Technologies used

- Python 3.9.21

- Django 4.2.20

- MySQL




## Features

- Generate short (tiny) URLs from long ones

- Redirect to the original URL using the short code

- View all stored links, including date of last usage

- Delete old links based on a time threshold

- Show the configuration of the shortening service
## API Reference

#### Create new short code

```http
  POST /api/v1.0/short/
```

| Argument | Type     
| :-------- | :------- 
| `long_link` | `URL`

#### Get link by code

```http
  GET /api/v1.0/short/${code}/
```

#### Get code by link

```http
  GET /api/v1.0/code/${long_link}/
```

#### Get all links

```http
  GET /api/v1.0/all/
```

#### Get server configuration

```http
  GET /api/v1.0/config/
```
#### Delete records by threshold
```http
  DELETE /api/v1.0/delete/{days}
```
(for now days are fixed at 30 and providing argument won't affect it)
## A quick demo
![DEMO](.assets/demo.gif)
