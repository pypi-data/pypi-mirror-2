
Domain management
=================

Basically, a domain in this system consists of the string representation of a DNS domain, and a reference to a user, the owner of the domain. It also has a "verified" mark, the semantics of which will be explained below. Any user can have any number of domains.

In XXX, if the user is not anonymous, there is a link labelled "add domain". Following it, the user is presented with `a form <TERENAPEERDOMAIN/domain/add>`_ to add a domain. In this form the user simply has to fill in the name of the domain, and click on the "add domain" button. This, however, is not enough to create a domain in the system. The system has to verify that the user has actual management rights over that domain in the DNS environment. To do this, after the user has submitted the domain creation form, it presents her with a page in which there is a special string, and a button labelled "verify ownership". The user has to create a page named with that string in the root of the HTTP service for that domain. Once she creates it, she has to click the "verify domain" button. The system then sends an HTTP GET request to ``http://<the new domain>/<the special string>``, and only when it gets a 200 OK response code, it considers the domain (and marks it as) verified.

A user can see a list of all her domains in `here <TERENAPEERDOMAIN/domain/>`_, where she can also verify her yet unverified domains.
