from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from .decorators import *
from .forms import BookingForm, CreateScoolForm, ExpressionForm, CreateExpressionForm
from .models import *

#####################
# GLOBAL PARAMETERS
#####################

ADMIN_EMAIL = "travellingtechbus@gmail.com"

#####################
# Common Views
#####################


def school_logout(request):
    """Redirect a user to login page after logout from the Platform

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponseRedirect to the appropriate URL for the arguments passed.
    :rtype: HttpResponseRedirect
    """
    logout(request)
    return redirect("login")


@unauthenticated_user
def school_login(request):
    """Render the login page for an unauthenticated user.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("admin-dashboard")
        else:
            messages.info(request, "E-mail OR password is incorrect")

    data = {}

    return render(request, "schoolApp/school-login.html", data)


