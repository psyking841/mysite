import re
import hmac
import random
import hashlib
from string import ascii_letters
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Post, User
from django.urls import reverse


secret = 'fart'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def make_salt(length = 5):
    return (''.join(random.choice(ascii_letters) for x in range(length)))

def make_pw_hash(name, password, salt = None):
    # nm = name
    # pw = password
    if not salt:
        salt = make_salt()
    h = hashlib.sha256((name + password + salt).encode('utf-8')).hexdigest()
    return '{},{}'.format(salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def login(request):
    if request.method == "GET":
        return render(request, 'blogs/login-form.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Look up users
        u = User.objects.get(username=username)
        if u and valid_pw(username, password, u.password):
            # response = blog_front(request)
            response = HttpResponseRedirect(reverse('blogs:welcome', kwargs={'username': username}))
            # response = HttpResponseRedirect('/blogs/welcome', {'username': 'AAA'})
            cookie_value = make_secure_val(u.id)
            response.set_cookie(key='user_id', value=cookie_value)
            return response
        else:
            msg = 'Invalid login'
            context = {
                'error': msg
            }
            return render(request, 'blogs/login-form.html', context)

def logout(request):
    response = HttpResponseRedirect('/blogs/signup')
    response.delete_cookie(key='user_id')
    return response

def blog_front(request):
    # block user WO cookie
    user_cookie = request.COOKIES.get('user_id')
    if not user_cookie:
        return HttpResponseRedirect(reverse('blogs:signup'))
    user_id, h = user_cookie.split('|')
    if not user_id.isdigit():
        return HttpResponseRedirect(reverse('blogs:signup'))
    if not h == hmac.new(secret.encode('utf-8'), user_id.encode('utf-8'),
             digestmod='sha256').hexdigest():
        return HttpResponseRedirect(reverse('blogs:signup'))

    latest_posts_list = Post.objects.order_by('-last_modified')[:5]
    context = {
        'posts': latest_posts_list,
    }
    return render(request, 'blogs/front.html', context)


def post_details(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {'post': post}
    return render(request, 'blogs/permalink.html', context)


def newpost(request):
    if request.method == "GET":
        return render(request, 'blogs/newpost.html')
    elif request.method == "POST":
        subject = request.POST['subject']
        content = request.POST['content']

        if subject and content:
            p = Post(subject=subject, content=content)
            p.save()
            return HttpResponseRedirect('/blogs/post/{post_id}'.format(post_id=p.id))
        else:
            error = "subject and content, please!"
            context = {
                'subject': subject,
                'content': content,
                'error': error
            }
            render("newpost.html", context)


def welcome(request, username):
    # context = {'username': request.GET['username']}
    context = {'username': username}
    return render(request, 'blogs/welcome.html', context)


def make_secure_val(val):
    return '{}|{}'.format(val,
                          hmac.new(secret.encode('utf-8'),
                                   str(val).encode('utf-8'),
                                   digestmod='sha256').hexdigest())


def register_user(name, password, email):
    """
    """
    pw_hash = make_pw_hash(name, password)
    return User(username=name,
                password=pw_hash,
                email=email)

# TODO: put it in DB
def signup(request, **kwargs):
    if request.method == "GET":
        return render(request, 'blogs/signup-form.html', kwargs)
    elif request.method == "POST":
        have_error = False
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST['verify']
        email = request.POST['email']

        params = {'username': username, 'email': email}

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            return render(request, 'blogs/signup-form.html', params)
        else:
            try:
                u = User.objects.get(username=username)
            except User.DoesNotExist:
                u = None
            if u:
                msg = 'That user already exists.'
                params['error_username'] = msg
                return render(request, 'blogs/signup-form.html', params)
            else:
                # This is new user
                u = register_user(name=username, password=password, email=email)
                u.save()
                rep = HttpResponseRedirect('/blogs/')
                rep.set_cookie(key='user_id', value=make_secure_val(u.id))
                return rep
