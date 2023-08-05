# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.comments.views import post_comment

@login_required
def post_comment_auth(request):
    return post_comment(request)