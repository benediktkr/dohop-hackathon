#! /usr/bin/env python2
# coding: utf8
import functools

import requests
import bottle
from bottle import route, request, response, get, post, abort, redirect
from bottle import jinja2_view, Jinja2Template, static_file, template, hook
from beaker.middleware import SessionMiddleware

from dohop import get_avg_range

def rule1(char):
    rules = {'&': '&amp;',
             '<': '&lt;',
             '>': '&gt;',
             '"': '&quot;',
             "'": '&#x27;',  # &aops; isn't in the html spec
             '/': '&#x2F;'}
    if char in rules:
        return rules[char]
    return char

def html_escape(text):
    encoded = [rule1(c) for c in text]
    return "".join(encoded)

view = functools.partial(jinja2_view,
                         navitems=[],
                         request=request,
                         session=lambda: request.environ.get('beaker.session'))

@get('/')
@view("index.jinja2")
def index():
    return {}

@post('/fares.json')
def fares():
    data = dict(request.forms)
    data['date_diff'] = 2
    print data
    #return get_avg_range(frm, to, day)
    return get_avg_range(**data)

## --- STATIC FILES ---
    
@get('/static/spinner.gif')
def getccjpg():
    return static_file('static/spinner.gif', '.')

@get('/static/cover.css')
def covercs():
    return static_file('static/cover.css', '.')

@get('/static/bootstrap.min.js')
def bootstrapjs():
    return static_file('static/bootstrap.min.js', '.')

@get('/static/index.js')
def indexjs():
    return static_file('static/index.js', '.')

@get('/static/bootstrap.min.css')
def bootstrapjs():
    return static_file('static/bootstrap.min.css', '.')

@get('/static/jquery.js')
def jqueryjs():
    return static_file('static/jquery.js','.')

application = bottle.app()
application = SessionMiddleware(application, {'session.type': 'memory',
                                              'session.cookie_expires': True,
                                              'session.auto': True,
                                              'session.cookie_expires': True,
                                              'session.httponly': True})
    
if __name__ == '__main__':
    bottle.run(app=application,
               host='0.0.0.0',
               port=3004,
               debug=True,
               reloader=True)

