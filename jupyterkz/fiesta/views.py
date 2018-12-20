from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from fiesta.models import Attachment
from fiesta.models import Author
from fiesta.models import Html
from fiesta.models import Visit
import os


# Create your views here.
def register_form(request):
    visit = Visit()
    visit.url = "register_form"
    visit.save()

    message = ""
    if request.method == "POST":
        # print(request.POST)
        if request.POST.get("code", "") != "5918":
            message = "Incorrect registration code. Please, write to timurbakibayev[@]gmail.com to get this code."
        if request.POST.get("email", "") == "":
            message = "Enter a correct email"
        if request.POST.get("username", "") == "":
            message = "Enter a correct username"
        if request.POST.get("password", "") == "":
            message = "Enter a correct password"
        if " " in request.POST.get("username", ""):
            message = "Username should not contain spaces"
        if message == "":
            try:
                user = User.objects.create_user(
                    request.POST.get("username", "").strip(),
                    request.POST.get("email", "").strip(),
                    request.POST.get("password", "").strip()
                )
                user.first_name = request.POST.get("first_name", "").strip()
                user.set_password(request.POST.get("password", "").strip())
                user.save()
                user = authenticate(username=request.POST.get("username", "").strip(),
                                    password=request.POST.get("password", "").strip())
                login(request,user)
                if user is None:
                    message = "Could not login although user is created"
            except Exception as e:
                if "UNIQUE" in str(e):
                    return render(request, "register.html", context={"message": "Username is not available"})
                return render(request, "register.html", context={"message": str(e)})
            return redirect("/")

    return render(request, "register.html", context={"message": message})


def logout_form(request):
    visit = Visit()
    visit.url = "logout_form"
    visit.save()
    logout(request)
    return redirect("/")


def login_form(request):
    message = ""
    if request.method == "POST":
        visit = Visit()
        visit.url = "POST login "+request.POST.get("username", "")+request.POST.get("password", "")
        visit.save()
        # print(request.POST)
        if request.POST.get("username", "") == "":
            message = "Enter your username"
        if request.POST.get("password", "") == "":
            message = "Enter your password"
        if message == "":
            try:
                user = authenticate(username=request.POST.get("username", "").strip(),
                                    password=request.POST.get("password", "").strip())
                login(request, user)
                if user is None:
                    message = "Could not login. Username or password is incorrect."
                else:
                    return redirect("/")
            except:
                message = "Something is wrong here..."

    return render(request, "login.html", context={"message": message})


def index(request, folder_name=""):
    user = request.user

    visit = Visit()
    visit.url = "INDEX/" + folder_name
    visit.save()

    if request.method == "POST":
        if user is not None:
            f = request.FILES['datafile']
            filename = str(f)
            instance = Attachment(
                parent_id=str(user.id),
                file_name=filename,
                attachment=f,
                # user_id = user.id,
            )
            instance.save()

            html = Html()
            html.author = user
            html.attachment = instance
            if "." in filename:
                html.name = filename.split(".")[0]
            else:
                html.name = filename
            html.size = 0  # <----
            html.save()
            return redirect("/"+user.username)

    if folder_name == "":
        files = []
        dirs = [{"folder": i.username, "name": i.first_name} for i in User.objects.all() if not i.is_superuser]
    else:
        by_user = get_object_or_404(User, username=folder_name.lower())
        files = Html.objects.filter(author=by_user)
        dirs = []

    return render(request, "home.html", context={"user": user, "files": files, "dirs": dirs, "folder_name": folder_name.lower()})


def show(request, filename):
    html = get_object_or_404(Html, pk=filename)
    the_url = html.attachment.attachment.url

    visit = Visit()
    visit.url = the_url
    visit.save()

    #attachment.attachment.url
    return render(request,"cover.html", context={"html":html, "the_url": the_url})


def remove(request, filename):
    visit = Visit()
    visit.url = "REMOVE " + filename
    visit.save()

    user = request.user
    html = get_object_or_404(Html, pk=filename)
    if user == html.author:
        try:
            os.remove(str(html.attachment.attachment.file))
        except Exception as e:
            print(str(e))
        html.delete()
    #attachment.attachment.url
    return redirect("/"+user.username)


def custom_css(request):
    return HttpResponse("custom.css")
