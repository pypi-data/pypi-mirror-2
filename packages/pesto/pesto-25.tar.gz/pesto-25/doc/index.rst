Pesto
======

.. testsetup:: *

        from pesto.testing import TestApp


Introduction
------------

Pesto is a library for Python web applications. Its aim is to make writing WSGI
web applications easy and fun. Pesto isn't a framework – how you integrate
with databases, what templating system you use or how you prefer to organize
your source files is up to you. Above all, Pesto aims to be small, well documented and
well tested.

Pesto makes it easy to:

    - Map any URI to any part of your application.
    - Produce unicode aware, standards compliant WSGI applications.
    - Interrogate WSGI request information – form variables and HTTP request headers.
    - Create and manipulate HTTP headers, redirects, cookies etc.
    - Integrate with any other WSGI application or middleware, giving you
      access to a vast and growing resource.

Contents:

.. toctree::
   :maxdepth: 2

   getting_started
   request
   response
   dispatch
   cookies
   session
   httputils
   wsgiutils
   utils
   caching



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Examples
---------

A very basic web application to demonstrate handling a request and creating a response:

.. testcode::

    from pesto import to_wsgi, Response

    def handler(request):
        return Response([
            "<html>",
            "<body><h1>Whoa Nelly!</h1></body>",
            "</html>",
        ])

    if __name__ == "__main__":
        from wsgiref import simple_server
        httpd = simple_server.make_server('', 8080, to_wsgi(handler))

Pesto handler functions typically take a ``Request`` object as an argument and
should return a ``Response`` object.

A longer example using the ``DispatcherApp`` class to map URLs to
handlers:

.. testcode::

    from pesto import Response
    from pesto.dispatch import DispatcherApp
    app = DispatcherApp()

    recipes = {
        'pesto': "Blend garlic, oil, parmesan and pine nuts.",
        'toast': "Put bread in toaster. Toast it."
    }

    @app.match('/', 'GET')
    def recipe_index(request):
        """
        Display an index of available recipes.
        """
        markup = ['<html><body><h1>List of recipes</h1><ul>']
        for recipe in sorted(recipes):
            markup.append(
                '<li><a href="%s">%s</a></li>' % (
                    show_recipe.url(recipe=recipe),
                    recipe
                )
            )
        markup.append('</ul></body></html>')
        return Response(markup)

    @app.match('/recipes/<recipe:unicode>', 'GET')
    def show_recipe(request, recipe):
        """
        Display a single recipe
        """
        if recipe not in recipes:
                return Response.not_found()

        return Response([
            '<html><body><h1>How to make %s</h1>' % recipe,
            '<p>%s</p><a href="%s">Back to index</a>' % (recipes[recipe], recipe_index.url()),
            '</body></html>'
        ])

    if __name__ == "__main__":
        from wsgiref import simple_server
        httpd = simple_server.make_server('', 8080, app)
        httpd.serve_forever()

.. doctest::
        :hide:

        >>> app = TestApp(app)
        >>> print app.get('/').body
        <html><body><h1>List of recipes</h1><ul><li><a href="http://localhost/recipes/pesto">pesto</a></li><li><a href="http://localhost/recipes/toast">toast</a></li></ul></body></html>
        >>> print app.get('/recipes/toast').body
        <html><body><h1>How to make toast</h1><p>Put bread in toaster. Toast it.</p><a href="http://localhost/">Back to index</a></body></html>
        >>> print app.get('/recipes/cheese').status
        404 Not Found


Development status
------------------

Pesto is production ready and used on a wide variety of websites.

To browse or check out the latest development version, visit
http://patch-tag.com/r/oliver/pesto. For documentation, visit http://pesto.redgecko.org/.

Mailing list
------------

A google groups mailing list is online at
http://groups.google.com/group/python-pesto. Please use this for any
questions or comments relating to Pesto.


Licence
--------

Pesto is available under the terms of the `new BSD licence <http://www.opensource.org/licenses/bsd-license.php>`_.

