#!/usr/bin/python

from flask import Flask, Response, request, redirect
from url_match import parse_url
import random

app = Flask(__name__)

dict = {}

id_charset = [chr(c) for c in list(range(48, 57)) + list(range(65, 90)) + list(range(97, 122))]
def generate_id(length: int) -> str:
    """
    Generates an alpha-numeric ID with the given length.
    """
    return ''.join(random.sample(id_charset, k=length))

def get_shortened_id(long_url: str) -> str:
    """
    Tries to get the shortened URL
    """
    try:
        return list(dict.keys())[list(dict.values()).index(long_url)]
    except ValueError:
        return None
    except AttributeError:
        return None

@app.errorhandler(404)
def route_404(e):
    # Don't do anything fancy, just send the 404
    return Response(status=404)

@app.route('/')
def route_index():
    """
    The index route. Nothing to see here, just 204s the request.
    """
    # TODO: Maybe serve a basic webpage with a box to make a URL from?
    #       For now just 204 it.
    return Response(status=204)

@app.route('/create/<path:url>')
def route_create(url: str):
    """
    Creates a new shortened URL to target the one provided.
    """
    url = url + str(request.query_string)
    id = get_shortened_id(url)
    if id:
        # return Response(status=403)
        return '<html><body><a href="{0}">{0}</a></body></html>'.format(request.url_root + id)

    # Try parse the URL, 403ing if it isn't valid
    if not parse_url(url, public=False):
        return Response(status=403)

    # Allocate a new ID, store the URL, and return the shortened one.
    id = generate_id(5)
    dict[id] = url
    return '<html><body><a href="{0}">{0}</a></body></html>'.format(request.url_root + id)

@app.route('/<id>')
def route_id(id: str):
    """
    Looks up the given ID and redirects to the corresponding URL.
    """
    if id in dict.keys():
        return redirect(dict[id])
        #return dict[id]
    return Response(status=404)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
