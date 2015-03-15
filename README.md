# Dohop hackathon

Dohop opened up access to an API for flight prices. 

Documentation here: http://www.dohop.com/hackathon/livestore-api.html

## My idea

When booking a flight, I find it hard to quantify the price unless it is a route I fly often. http://www.dohop.com/hackathon/livestore-api.html

Originally I wanted to use historic prices to quantify the given price, but this is not available through the API. My program searches for flights 30 days (adjustable) before and 30 days after the entered date, and uses this information to help the use quantify prices.  

Example usage:

    $ python dohop.py KEF HAM,LBC,XFW 2015-06-15
    {'average': 27797,
     'cheapest_date': '2015-06-05',
     'cheapest_price': 9573,
     'expensive_date': '2015-08-20',
     'expensive_price': 59149,
     'my_price': 16061,
     'price_count': 106}
    
   Good price!
   $

Currently it's only a python cli script, might be turned into a basic website. 

### Known limitations:

If there is no flight the given day, then `my_price` is `None`, rather than showing the closest match. 

## Limitations of the API

It seems like the API doesn't include prices that are more than 7 months into the future. At the time of writing, Marc 2015, prices to Hamburg in December 2015 are unavailable in this API, but available on Dohop.com. 

Further, the API doesn't return what airline a specific fare is with, nor what time of day or how long the flight is. 

Historical prices are unavailable. 

Only one fare (the cheapest) is returned for a given date range. 

This is fine and understandable, but worth nothing. 