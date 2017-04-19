from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
from django.contrib import auth
from . import twitter_db
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
import re
from django.views.static import serve
import os
import os.path
import mimetypes
from django.http import HttpResponse

# Create your views here.


def lalka(request):
    dick = {
    }
    return render(request, 'lalka.html', dick)

def static(request):
    base = os.path.basename(request.path)
    file_path = request.path.replace("static", "assets")
    file_path = os.path.abspath(file_path[1:])
    with open(file_path, 'rb') as fp:
            file = fp.read()
    response = HttpResponse(
        file, content_type=mimetypes.guess_type(request.path)[0])
    response['Content-Disposition'] = 'attachment; filename="' + base + '"'
    return response

def update_form(request):
    view = "update_form"
    if request.user.is_authenticated():
        twid = re.search("/twit/update/form/(\d+)", request.path).group(1)
        dick = {
            'delete_twit': '/twit/delete/',
            'update_form': '/twit/update/form/',
            'update_db': '/twit/update/db/',
            'send_link': '/twit/add/',
            'logout': '/logout/',
            'articles': twitter_db.read_data_from_sql(request.user)
        }
        twit = twitter_db.take_twit_by_id(id=twid)
        dick['twit_update_text'] = twit.twitter_text
        dick['twit_update_id'] = int(twid)
        return render(request, 'forms.html', dick)
    return redirect('/auth/')


def update_db(request):
    view = "update_db"
    if request.user.is_authenticated():
        if request.method == "POST":
            twitter_db.update_data(
                twi_id=str(request.POST['update_id']),
                new_twit=request.POST['text'])
            return redirect('/blog/')
    return redirect('/auth/')


def delete_twit(request):
    view = "delete_twit"
    if request.user.is_authenticated():
        twitter_db.delete_data_from_sql(
            user=request.user,
            row_id=re.search("/twit/delete/(\d+)", request.path).group(1)
        )
        return redirect('/blog/')
    redirect('/auth/')


def add_twit(request):
    view = "add_twit"
    if request.user.is_authenticated():
        if request.method == "POST":
            twitter_db.add_data_to_sql(
                user=request.user,
                twit=request.POST["text"])
        return redirect('/blog/')
    redirect('/auth/')


def blog(request):
    if request.user.is_authenticated():
        view = "blog"
        dick = {
            'twit_update': None,
            'delete_twit': '/twit/delete/',
            'update_form': '/twit/update/form/',
            'send_link': '/twit/add/',
            'logout': '/logout/',
            'articles': twitter_db.read_data_from_sql(request.user)
        }
        return render(request, 'forms.html', dick)
    return redirect('/auth/')


def registration(request):
    view = "registration"
    dick = {"DOMEN": request.path_info}
    if request.method == "POST":
        if "username" in request.POST:
            newuser_form = UserCreationForm(request.POST)
            if newuser_form.is_valid():
                newuser_form.save()
                newuser = auth.authenticate(
                    username=newuser_form.cleaned_data['username'],
                    password=newuser_form.cleaned_data['password2']
                )
                auth.login(request, newuser)
                request.session.set_expiry(1000)
                request.session["twit"] = True
                return redirect("/blog/")

            else:
                dick['error'] = regerror(str(newuser_form))

    if request.method == "GET":
        dick['error'] = False
    return render(request, 'registration.html', dick)


def authentefication(request):
    view = "authentefication"
    dick = {
        "DOMEN": request.path_info,
        "reg_page": '/reg/'}
    if "twit" in request.session:
        return redirect('/blog')

    if request.method == "POST":
        if "enter_email" in request.POST:
            username = request.POST.get("enter_email", '')
            password = request.POST.get("password", '')
            user = auth.authenticate(
                username=username,
                password=password
            )
            if user is not None:
                auth.login(request, user)
                request.session.set_expiry(1000)
                request.session["twit"] = True
                return redirect("/blog/")

            if user is None:
                dick['username'] = user
                return render(request, 'authorisation.html', dick)

    dick['username'] = "tmp_user"
    return render(request, 'authorisation.html', dick)


def logout(request):
    auth.logout(request)
    return redirect('/auth/')


def regerror(form):
    pat = re.search('<ul class="errorlist"><li>(.*?)</li></ul>', form)
    return pat.group(1)
