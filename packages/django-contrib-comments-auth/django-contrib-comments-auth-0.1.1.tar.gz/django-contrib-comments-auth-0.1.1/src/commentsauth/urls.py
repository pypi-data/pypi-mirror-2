from django.conf.urls.defaults import *
from commentsauth.views import post_comment_auth

urlpatterns = patterns('',
    url(r'^post/$', post_comment_auth, name='comments-post-comment-auth') 
)
