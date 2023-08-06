RestDyn
=======

RestDyn is a dynamic rest client built on top of the excellent restkit_ library.

.. _restkit : http://github.com/benoitc/restkit

It aims to be able to handle any uris for any apis.

How it work ?
-------------

Let's say we want to fetch the json API of the great service http://www.example.com. Their api is served from http://api.example.com/1.0/::

    >>> from restdyn import Client
    >>> ExampleAPI = Client('http://api.example.com/1.0/')

Now we want to get the result from http://api.example.com/1.0/users/search?q=Timy::

    >>> results = ExampleAPI.users.search(q='Timy')

That's it ! `results` is a json object.

Going further
-------------

Adding arguments automatically
++++++++++++++++++++++++++++++

Sometimes some api are a bit tricky. Previously, the version of the api was part of the resource but what if we have to specify it for each request::

    http://api.example.com/user/search?v=1.0&q=Timy

We can specify one or more params which will be automatically add to the query::

    >>> ExampleAPI = Client('http://api.example.com')
    >>> ExampleAPI.set_persistent_params(v="1.0")

or you can pass a dict::

    >>> ExampleAPI.set_persistent_params({'v':'1.0'})


Customize resources
+++++++++++++++++++

Some apis like Twitter add `.json` after the resource but before the query : https://api.twitter.com/1/search.json&q=Timy. We can do it like this::

    >>> TwitterAPI = Client('https://api.twitter.com/1', end_resource='.json')
    >>> results = TwitterAPI.search(q='Timy')

Post process result
+++++++++++++++++++

Sometimes you may have to clean up the result before send it back. You can do it by overloading the `Client.post_process_result` method.

Example:

    Google's web service won't send an http error 400 if the request failed. Instead, it will send a custom result::

        http://ajax.googleapis.com/ajax/services/search/web?q=Earth%20Day

will send back::

    {"responseData": null, "responseDetails": "invalid version", "responseStatus": 400}

Let's say we want to catch the error and raise an RequestFailed exception with a custom message which is in the "responseDetails" field::

        class CustomGoogleAPI(Client):
            def post_process_result(self, result):
                if result["responseStatus"] == 400:
                    raise RequestFailed(result['responseDetails'])
                return result

That's it ! Don't forget to return the result at the end of the `post_process_result` method.

        >>> GoogleAPI = CustomGoogleAPI('http://ajax.googleapis.com/ajax/services')
        >>> GoogleAPI.search.web(q="toto")
        Traceback (most recent call last):
        ...
        RequestFailed: invalid version

Adding a trailing slash
+++++++++++++++++++++++

If the api you are dealing have a slash in all its urls, you can configure restdyn to add it::

    >>> example_api = Client('http://api.example.com', add_trailing_slash=True)
