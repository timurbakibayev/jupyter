from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from fiesta.models import Attachment
from fiesta.models import Author
from fiesta.models import Html


# Create your views here.
def register_form(request):
    message = ""
    if request.method == "POST":
        # print(request.POST)
        if request.POST.get("email", "") == "":
            message = "Enter a correct email"
        if request.POST.get("username", "") == "":
            message = "Enter a correct username"
        if request.POST.get("folder", "") == "":
            message = "Enter a correct folder"
        if request.POST.get("password", "") == "":
            message = "Enter a correct password"
        if " " in request.POST.get("username", ""):
            message = "Username should not contain spaces"
        if " " in request.POST.get("folder", ""):
            message = "Username should not contain spaces"
        if message == "":
            try:
                user = User.objects.create_user(
                    request.POST.get("username", "").strip(),
                    request.POST.get("email", "").strip(),
                    request.POST.get("password", "").strip()
                )
                user.first_name = request.POST.get("first_name", "").strip()
                user.last_name = request.POST.get("folder", "").strip().lower()
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

    return render(request, "register.html", context={"message": message})


def login_form(request):
    message = ""
    if request.method == "POST":
        # print(request.POST)
        if request.POST.get("username", "") == "":
            message = "Enter your username"
        if request.POST.get("password", "") == "":
            message = "Enter your password"
        if message == "":
            user = authenticate(username=request.POST.get("username", "").strip(),
                                password=request.POST.get("password", "").strip())
            login(request, user)
            if user is None:
                message = "Could not login. Username or password is incorrect."
            else:
                return redirect("/")

    return render(request, "login.html", context={"message": message})


def index(request, folder_name=""):
    user = request.user

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
            html.name = filename
            html.size = 0  # <----
            html.save()
            return redirect("/"+user.last_name)

    if folder_name == "":
        files = []
        dirs = [i.last_name for i in User.objects.all() if i.last_name != ""]
    else:
        by_user = get_object_or_404(User, last_name=folder_name.lower())
        files = Html.objects.filter(author=by_user)
        dirs = []

    return render(request, "home.html", context={"user": user, "files": files, "dirs": dirs})
