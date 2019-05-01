import re
import traceback
"""
You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division


Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    try:
        total_sum = "0"
        total_sum = sum(map(int, args))
    except (ValueError, TypeError):
        no_sum = "Unable to calculate a sum:please provide integer operands."
        return no_sum

    return str(total_sum)

def multiply(*args):
    try:
        total = 1
        for i in map(int, args):
            total = total*i
    except (ValueError, TypeError):
        total= "Unable to calculate a sum:please provide integer operands."
    return str(total)

def subtract(*args):
    try:
        a = int(args[0])
        b = int(args[1])
        total = a - b
    except (ValueError, TypeError):
        total= "Unable to calculate a sum:please provide integer operands."

    return str(total)

def divide(*args):
    try:
        a = int(args[0])
        b = int(args[1])
        total = a / b
    except (ValueError, TypeError):
        total= "Unable to calculate a sum:please provide integer operands."
    except ZeroDivisionError:
        total = "You can not devide 0"
    return str(total)

def instruction():
    return "'The_calculation_you_want/number_1/number_2',it will return the result accordingly, add/1/2 -> 3"


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '': instruction,
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide': divide,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = '404 Not Found'
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
