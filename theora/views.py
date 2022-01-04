import re
import hmac
import random
import hashlib
from string import ascii_letters
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import NewsFeed, User
from django.urls import reverse

secret = 'fart'
invitation_code = 'invite-me-VIP'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


def make_salt(length=5):
    return (''.join(random.choice(ascii_letters) for x in range(length)))


def make_pw_hash(name, password, salt=None):
    # nm = name
    # pw = password
    if not salt:
        salt = make_salt()
    h = hashlib.sha256((name + password + salt).encode('utf-8')).hexdigest()
    return '{},{}'.format(salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


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


def login(request):
    if request.method == "GET":
        return render(request, 'theora/login-form.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Look up users
        u = User.objects.get(username=username)
        if u and valid_pw(username, password, u.password):
            response = HttpResponseRedirect(reverse('theora:welcome', kwargs={'username': username}))
            cookie_value = make_secure_val(u.id)
            response.set_cookie(key='user_id', value=cookie_value)
            return response
        else:
            msg = 'Invalid login'
            context = {
                'error': msg
            }
            return render(request, 'theora/login-form.html', context)


def logout(request):
    response = HttpResponseRedirect('/theora/signup')
    response.delete_cookie(key='user_id')
    return response


def welcome(request, username):
    # context = {'username': request.GET['username']}
    context = {'username': username}
    return render(request, 'theora/welcome.html', context)


def theora_front(request):
    # block user WO cookie
    user_cookie = request.COOKIES.get('user_id')
    if not user_cookie:
        return HttpResponseRedirect(reverse('theora:signup'))
    user_id, h = user_cookie.split('|')
    if not user_id.isdigit():
        return HttpResponseRedirect(reverse('theora:signup'))
    if not h == hmac.new(secret.encode('utf-8'), user_id.encode('utf-8'),
                         digestmod='sha256').hexdigest():
        return HttpResponseRedirect(reverse('theora:signup'))

    latest_posts_list = NewsFeed.objects.order_by('-pub_date')[:5]
    context = {
        'posts': latest_posts_list,
    }
    return render(request, 'theora/theora-front.html', context)


def signup(request, **kwargs):
    if request.method == "GET":
        return render(request, 'theora/signup-form.html', kwargs)
    elif request.method == "POST":
        have_error = False
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST['verify']
        email = request.POST['email']
        invitation = request.POST['invitation']

        params = {'username': username, 'email': email}

        if not invitation or invitation != invitation_code:
            params['error_invitation'] = "You need an invitation code for sign up."
            have_error = True

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
            return render(request, 'theora/signup-form.html', params)

        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            u = None
        if u:
            msg = 'That user already exists.'
            params['error_username'] = msg
            return render(request, 'theora/signup-form.html', params)
        else:
            # This is new user
            u = register_user(name=username, password=password, email=email)
            u.save()
            rep = HttpResponseRedirect('/theora/')
            rep.set_cookie(key='user_id', value=make_secure_val(u.id))
            return rep


def aboutme(request):
    return render(request, 'theora/about-me.html')