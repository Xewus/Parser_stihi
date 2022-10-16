## Start into **parser/**

### Must be placed inside **parser/** :

- `parser/scrapy.cfg`
- `parser/.env`  with **Flask** settings
 ***


 ## Start outside **parser/**

 ### Must be placed outside **parser/**

- `parser/scrapy.cfg`
- `parser/.env`  with **Flask** settings
 ***

### Aviable commands:
- Start Flask:
```
flask run
```
- Start Scrapy:
```
scrpy crawl <spider's name> -a author=<author>
```
```
scrpy crawl <spider's name> -a author=<author> urls=<url1#url2...>
```

### The Flask application has two endpoints:

- *server availability*
```
/test/
```
- *start parsing*

```
/scrapy/?spider=<spider's name>&author=<ivanov>
```
***
### Results of parsing will be saving into **parser/results/**.