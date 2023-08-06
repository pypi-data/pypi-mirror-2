Flea documentation contents
||||||||||||||||||||||||||||

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
        :maxdepth: 3

.. include:: ../README.txt


Overview
===========

The ``TestAgent`` class provides a user agent that can drive a WSGI
application::

	>>> from flea import TestAgent
	>>> agent = TestAgent(my_wsgi_app)

You can now use this agent to navigate your WSGI application by...


.. testsetup:: *

        from pesto.request import Request
        from pesto.response import Response
        from pesto.testing import make_environ
        from pesto.wsgiutils import mount_app
        from flea import TestAgent

        def redirect_app(environ, start_response):
                return Response.redirect('/')(environ, start_response)

        agent = TestAgent(
                mount_app({
                        '/': Response(["""
                                                <a id="mylink" href="/">foo</a>
                                                <form name="login-form" action="/"><input type='text' name='username'/><input type='text' name='password'/></form>
                                                <form name="contact" action="/"><button type="submit" name="send"/></form>
                                                <form name="register" action="/register"></form>
                                                <form name="upload" action="/">
                                                        <input type="file" name="image"/>
                                                        <input type="text" name="title"/>
                                                        <input type="radio" name="size" value="small"/>
                                                        <input type="radio" name="size" value="medium"/>
                                                        <input type="radio" name="size" value="large"/>
                                                        <input type="checkbox" name="spam_me" value="lots"/>
                                                        <input type="checkbox" name="terms_and_conditions" value="yes"/>
                                                        <select name="days" multiple="">
                                                                <option value="monday">monday</option>
                                                                <option value="tuesday">tuesday</option>
                                                                <option value="wednesday">wednesday</option>
                                                                <option value="thursday">thursday</option>
                                                                <option value="friday">friday</option>
                                                        </select>
                                                        <select name="color">
                                                                <option value="red">red</option>
                                                                <option value="green">green</option>
                                                        </select>
                                                </form>
                        """]),
                        '/register': redirect_app,
                })
        ).get('/')

...making GET requests:

.. doctest::

	>>> agent = agent.get('/my-page')

...making POST requests:

.. doctest::

	>>> agent = agent.post('/contact', data={'message': 'your father smells of elderberries'})

...clicking links:

.. doctest::

	>>> # Click on first <a> tag on page
	>>> agent = agent["//a[1]"].click()

	>>> # Click on first <a> tag with content 'foo'
	>>> agent = agent["//a[.='foo']"].click()

	>>> # Click on tag with id 'mylink'
	>>> agent = agent["//a[@id='mylink']"].click()

...and submitting forms:

.. doctest::

	>>> agent["//input[@name='title']"].value = 'picture of me on holiday'
	>>> agent = agent["//form[@name='login-form']"].submit()
	>>> agent = agent["//form[@name='contact']//button[@name='send']"].submit()


Filling and submitting forms
=============================

Any HTML form input or text area can be assigned a value by setting the
``.value`` property of the element:

.. doctest::

	>>> agent["//input[@name='title']"].value = 'apples'

Checkboxes
-----------

To turn checkboxes on and off, you need to assign to the ``.checked`` property:

.. doctest::

	>>> agent["//input[@name='terms_and_conditions']"].checked = True
	>>> agent["//input[@name='spam_me']"].checked = False


Select boxes and radio buttons
------------------------------

The ``.value`` property also works for select boxes and radio buttons:

.. doctest::

	>>> agent["//select[@name='color']"].value = 'red'

You'll get an error if you choose a value that doesn't correspond to one of the
select box or radio button options.

For multiple select boxes, you need to pass a list (or other iterable) of values:

.. doctest::

	>>> agent["//select[@name='days']"].value = ['monday', 'wednesday']

You can also toggle the ``.selected`` property of individual select box options:

.. doctest::

	>>> agent["//select[@name='color']/option[@value='red']"].selected = True


and likewise the ``.checked`` property on radio buttons:

.. doctest::

	>>> agent["//input[@name='size' and @value='small']"].checked = True

File uploads
-------------

To test file upload fields, you must assign a tuple of ``(filename,
content-type, data)`` to the ``.value`` property. The data part can either be a
string:

.. doctest::

	>>> agent["//input[@name='image']"].value = ('icon.png', 'image/jpeg', 'testdata')


Or a file-like object:

        >>> from StringIO import StringIO
        >>> f = StringIO('aaabbbccc')
	>>> agent["//input[@name='image']"].value = ('icon.png', 'image/png', f)


Filling forms in a single call
------------------------------

The ``.fill`` method is a useful shortcut for filling in an entire form with
just a single method call. Keyword arguments are used to populate input
controls by id or name:


.. doctest::

	>>> agent = agent["//form[@name='login-form']"].fill(
        ...     username='fred',
        ...     password='secret'
        ... ).submit()

Xpath expressions may be used for fields whose names can't be represented as
python identifiers or when you need more control over exactly which fields are
selected:

.. doctest::

	>>> agent = agent["//form[@name='login-form']"].fill(
        ...     ('input[1]', 'fred'),
        ...     ('input[2]', 'secret'),
        ... ).submit()

Currently the ``.fill`` method does not work for setting checkboxes.

CSS selectors
--------------

Don't like XPath? You can use CSS selectors instead::

	>>> agent = agent.findcss("a").click()
	>>> agent = agent.findcss("a.highlighted").click()
	>>> agent = agent.findcss("a#mylink").click()


HTTP redirects
--------------

HTTP redirect responses (301 or 302) are followed by default. If you want to
explicitly check for a redirect, you'll need to specify ``follow=False`` when
making the request. All methods associated with making a request - ``click``,
``submit``, ``get``, ``post`` etc - take this parameter.

To follow a redirect manually:
 
 	>>> agent = agent["//form[@name='register']"].submit(follow=False)
        >>> assert agent.response.status_code == 302
 	>>> agent = agent.follow()
 

Querying WSGI application responses
-----------------------------------

Checking the content of the request
`````````````````````````````````````

::

	>>> assert agent.request.path_info == '/index.html'
	>>> print agent.request.environ
        {...}

``agent.request`` is a `pesto.request.Request <http://pypi.python.org/pypi/pesto>`_
object, and all attributes of that class are available to examine.

Checking the content of the response
`````````````````````````````````````

::

	>>> assert agent.response.content_type == 'text/html'
	>>> assert agent.response.status == '200 OK'

Note that ``agent.response`` is a `pesto.testing.TestResponse
<http://pypi.python.org/pypi/pesto>`_ object, and all attributes of that class
are available.


By default, responses are checked for a successful status code (2xx or 3xx),
and an exception is raised for any other status code. If you want to bypass
this checking, use the ``check_status`` argument:

.. doctest::

        >>> def myapp(environ, start_response):
        ...     start_response('500 Error', [('Content-Type', 'text/plain')])
        ...     return ['Sorry, an error occurred']
        ...
        >>> TestAgent(myapp).get('/')
        Traceback (most recent call last):
        ...
        BadStatusError: GET '/' returned HTTP status '500 Error'
        >>> TestAgent(myapp).get('/', check_status=False)
        <flea.TestAgent ...>


Checking returned content.
``````````````````````````````

The ``.body`` property contains the raw response
from the server::
	
	>>> assert 'you are logged in' in agent.body

Any element selected via an xpath query has various helper methods useful for
inspecting the document.

Checking if strings are present in an HTML element
``````````````````````````````````````````````````

::

	>>> assert 'Welcome back' in agent['//h1']

Accessing the html of selected elements
```````````````````````````````````````

::

	>>> agent['//p[1]'].html()
	<p>Eat, drink and be <strong>merry!</strong></p>

Note that this is the html parsed and reconstructed by lxml, so is unlikely to
be the literal HTML emitted by your application - use ``agent.body`` for that.

Accessing textual content of selected elements
````````````````````````````````````````````````
::

	>>> agent['//p[1]'].striptags()
	Eat, drink and be merry!

Inspecting and interacting with a web browser
---------------------------------------------

Flea gives you two methods for looking at what's going on in your application
in a web browser.

The ``showbrowser`` method opens a web browser and displays the content of the
most recently loaded request::

        >>> agent.get('/').showbrowser()

The ``serve`` method starts a HTTP server running your WSGI application and
opens a web browser at the location corresponding to the most recent request.
For example, the following code causes a web browser to open at
``http://localhost:8080/foobar``::

        >>> agent.get('/foobar').serve()

If you want to change the default hostname and port for the webserver you must
specify these when first initializing the ``TestAgent`` object::

	>>> agent = TestAgent(my_wsgi_app, host='192.168.1.1', port='8888')
        >>> agent.get('/foobar').serve()

Now the web browser would be opened at ``http://192.168.1.1:8888/foobar``.

One final note: the first request to the application is handled by relaying the
most recent response received to the web browser, including any cookies
previously set by the application. Also, if any methods have been called
that access the lxml representation of an HTML response – eg finding elements
by an XPath query or filling form fields – then the lxml document in its
current state will be converted to a string and served to the browser, meaning
that while the document should be logically equivalent, it will no longer be a
byte-for-byte copy of the response received from the WSGI application.

This **only** applies to the first request, and ensures that the web browser
receives a copy of the page as currently in memory, with any form fields
filled in and with all any cookies set so that you can pick up in your web
browser exactly where the ``TestAgent`` object left off.

API documention
----------------

.. automodule:: flea
        :members:

