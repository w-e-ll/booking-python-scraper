# Booking Python Spider

This Scraper collects useful sections of data such as room facilities and hotel nearby locations (Area Info) for hotel content generation.

You have next functionality:
* script loads hotel names and ids from already prepared file: tb_hotels.json
* gets section of room facilities
* gets section of hotel nearby (Area Info).
* after all content preparation has been accomplished, script dumps data to a json file

## How to start
Dependencies

* Python3
* Selenium

To install requirements and start the application:

```
$ virtualenv -p python3.6 booking_scraper
$ cd booking_scraper
$ activate it (source bin/activate)
$ git clone https://github.com/w-e-ll/booking-spider.git
$ cd booking-spider
$ pip install -r requirements.txt
$ python booking.py
```

## TODO:
* scrape hotel description
* scrape most popular facilities
* scrape attractions recommended by locals
* house rules

made by: https://w-e-ll.com
