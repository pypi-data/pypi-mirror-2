Flea
====

Flea helps you write functional tests for WSGI applications without needing to start
an HTTP server.

Flea is fully integrated with lxml's XPath api, making it easy to inspect,
modify and navigate HTML documents returned from your WSGI application. Here's
an example session::

	>>> agent = TestAgent(my_wsgi_app)
	>>> agent.get('/')
	>>> print agent.body
	<html>
		<body>
			<a href="/sign-in">sign in</a>
		</body>
	</html>
	>>> agent = agent["//a[.='sign in']"].click()
	>>> print agent.request.request_uri
	http://localhost/sign-in
	>>> agent["//input[@name='username']"].value = 'root'
	>>> agent["//input[@name='password']"].value = 'password'
	>>> agent = agent["//input[@type='submit']"].submit()

