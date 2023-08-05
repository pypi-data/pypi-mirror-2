README
======

To make sure no bad hacker adds a comment with no authentication, you have to install a small app called django-contrib-comments-auth::

	pip install django-contrib-comments-auth
	
Add it to the INSTALLED_APPS::

 	INSTALLED_APPS = (
    # ...
    'commentsauth',
	)
	
Add one line to your root-urls.py::

	urlpatterns = patterns('',
    # ...
    (r'^comments/', include('commentsauth.urls'),
    (r'^comments/', include('django.contrib.comments.urls'))
	)
	
It must be *before* the django.contrib.comments.urls-directive and have the same prefix. That's it.

