BasicHttp
=========

A easy to use and clean HTTP client lib for Python.

Description
-----------

BasicHttp is based on httplib.

How to use
----------

>>> from basic_http import BasicHttp
>>> request = BasicHttp('http://www.example.com/')
>>> response = request.GET()
>>> response
{
    'status': 200,
    'header': {
        'Content-Length': '596',
        'Server': 'Apache',
        'Content-Type': 'text/html; charset=UTF-8',
    },
    'body': '...You have reached this web page by ...'
}

Params
------
data: string: raw XML or JSON document.
      dict: key-value Python dictionary.

headers: dict: key-value Python dictonary with HTTP request headers

wanted_status: list: value Python list with HTTP status code expected

Examples
--------

>>> from basic_http import BasicHttp
>>> request = BasicHttp('http://www.example.com/')
>>> request.authenticate('user', 'pass')
>>> response = request.GET(headers={'Accept': application/json})

>>> request = BasicHttp('http://www.example.com/')
>>> request.authenticate('user', 'pass')
>>> response = request.POST(data='raw XML here.', wanted_status=[201,202])

>>> request = BasicHttp('http://www.example.com/')
>>> request.authenticate('user', 'pass')
>>> response = request.PUT(data={'id': 5, 'name': example}, wanted_status=[201,202])

