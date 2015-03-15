from datetime import date, timedelta
from requests import get, post, put
from pprint import pprint
import json
import sys

USER_COUNTRY = "IS/"
API = 'http://api.dohop.com/api/v1/livestore/en/' + USER_COUNTRY
CURRENCY = "ISK"

## -- Exceptions

class FareError(Exception):
    pass

## -- Helpers
def date_range(start, end):
    d = date(*map(int, start.isoformat().split('-')))
    while d < end:
        yield d
        d = d + timedelta(1)

def get_isk_price(fare):
    if 'conv_fare' in fare:
        return int(round(fare['conv_fare']))
    else:
        return int(round(fare['f']))        

def usage():
    return """python dohop.py FROM_AIRPORT ARRIVAL_AIRPORTS DATE

Example: python dohop.py KEF HAM 2015-12-26
         python dohop.py KEF HAM,FRA,TXL,SXF 2015-12-26"""
        
## -- Interaction with Dohop api

def get_avg_range(frm, to, day, stay=None, date_diff=180):
    day_date = date(*map(int, day.split('-')))
    max_day = day_date + timedelta(date_diff)
    min_day = day_date - timedelta(date_diff)
    if type(stay) == list:
        stay = ",".join(return_after)
    if type(to) == list:
        to = ",".join(to)

    prices = dict()
    
    for d in date_range(min_day, max_day):
        isodate = d.isoformat()
        res = get_for_day(frm, to, isodate, stay)
        try:
            price = min([get_isk_price(a) for a in res['fares']])
            prices[isodate] = price
        except ValueError:
            pass

    if len(prices) == 0:
        raise FareError("No fares found")
    avg_f = sum(prices.values()) / len(prices)
    avg = int(round(avg_f))

    expensive_date = max(prices, key=prices.get)
    cheapest_date = min(prices, key=prices.get)
    
    return {'average': avg,
            'cheapest_date': cheapest_date,
            'cheapest_price': prices[cheapest_date],
            'expensive_date': expensive_date,
            'expensive_price': prices[expensive_date],
            'prices': prices,
            'price_count': len(prices),
            'my_price': prices[day] if day in prices else None}

def get_for_day(frm, to, day, stay=None):
    include_split = bool(stay)

    request = {'currency': CURRENCY,
               'fare-format': 'full',
               'from_airport': frm,
               'arrival_airports': to,
               #'wd': '12345', # monday = 1
               'date_from': day,
               'date_to': day,
               'stay': stay,
               'include_split': include_split,
               'n_max': 100}
    uri='per-airport/{from_airport}/{arrival_airports}/{date_from}/{date_to}'
    uri=API+uri.format(**request)
    json = get(uri, params=request).json()

    if "error" in json:
        raise FareError(json["error"])
    return json

if __name__ ==  "__main__":
        #j = get(API+'per-airport/KEF/TXL,SXF,FRA,HAM/2016-12-26/2016-12-27',
    #        params=params).json()
    #pprint(j)

    if not len(sys.argv) == 4:
        print usage()
        sys.exit(1)
    
    try:
        j = get_avg_range(sys.argv[1], sys.argv[2], sys.argv[3])
        del j['prices']
        pprint(j)
        print
        if j['my_price'] < j['average']:
            print "Good price!"
        else:
            print "Bad price!"
    except FareError as error:
        print error
