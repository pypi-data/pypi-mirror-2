README
======

To make sure no bad hacker adds a comment with no authentication, you have to install a small app called django-contrib-comments-auth::

	pip install django-contrib-comments-auth
	
Add it to the INSTALLED_APPS::

 	INSTALLED_APPS = (
    # ...
    'django.contrib.comments',
    'commentsauth',
	)
	
Add these lines to your root urls.py::

	urlpatterns = patterns('',
    # ...
    (r'^comments/', include('commentsauth.urls'),
    (r'^comments/', include('django.contrib.comments.urls'))
	)
	
It must be *before* the django.contrib.comments.urls-directive and have the same prefix. 

The template for the comment-form could look like::

	{% load comments %}
	{% if request.user.is_authenticated %}
	<h2>Leave a comment</h2>
	{% get_comment_form for object as form %}
    <form action="{% comment_form_target %}" method="POST"> 
	{{ form.comment }} 
	{{ form.honeypot }} 
	{{ form.content_type }} 
	{{ form.object_pk }} 
	{{ form.timestamp }} 
	{{ form.security_hash }} 
	<input type="submit" value="Add comment" id="id_submit" />
	</form> 
	{% else %}
	<h1>Display login form or link to login page!</h1>
	{% endif %}
	
Please make sure to have these two lines in your MIDDLEWARE_CLASSES::

	MIDDLEWARE_CLASSES = (
	# ...
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
	)

	

