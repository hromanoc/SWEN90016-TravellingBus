from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect, render

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

#####################
# AUTO EMAILS 
#####################


def send_email_expression(email, expression):
    """Send an email after an expression is created

    :param email: email of the administrator
    :type email: string
    :param expression: An expression of interest
    :type expression: Expression
    """
    template = get_template("schoolApp/admin-email-expression.html")
    data = {"email": email, "expression": expression}
    content = template.render(data)

    email = EmailMultiAlternatives(
        "🚌 A New Expression of Interest! 🚌",
        "Travelling Technology Bus",
        ADMIN_EMAIL,
        [email],
    )

    email.attach_alternative(content, "text/html")
    email.send()


def send_email_expression_confirmation(email, expression):
    """Send an email to a school representative after an expression is confirmed

    :param email: email of the administrator
    :type email: string
    :param expression: An expression of interest
    :type expression: Expression
    """
    template = get_template("schoolApp/admin-email-expression-confirmation.html")
    data = {"expression": expression}
    content = template.render(data)

    email = EmailMultiAlternatives(
        "🚌 Expression of Interest has been confirmed! 🚌",
        "Travelling Technology Bus",
        ADMIN_EMAIL,
        [email],
    )

    email.attach_alternative(content, "text/html")
    email.send()


def send_email_booking_cancellation(email, booking):
    """Send an email after a booking has been cancelled

    :param email: email of the user
    :type email: string
    :param booking: A school's booking
    :type booking: string
    """
    template = get_template("schoolApp/admin-email-booking-cancellation.html")
    data = {"booking": booking}
    content = template.render(data)

    email = EmailMultiAlternatives(
        "🚨🚌 A Booking has been cancelled =(! 🚌🚨",
        "Travelling Technology Bus",
        ADMIN_EMAIL,
        [email],
    )

    email.attach_alternative(content, "text/html")
    email.send()

