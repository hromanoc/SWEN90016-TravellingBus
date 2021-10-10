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
#####################
# Admin's Views
#####################


@login_required(login_url="login")
@admin_only
def admin_dashboard(request):
    """Render the admin dashboard page for an admin user.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    expressions_list = Expressions.objects.all()
    bookings_list = Booking.objects.all()

    data = {"expressions": expressions_list, "bookings": bookings_list}

    return render(request, "schoolApp/admin-dashboard.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def admin_expressions(request):
    """Render the admin expression of interests list page for an admin user.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    expressions_list = Expressions.objects.all()

    data = {"expressions": expressions_list}

    return render(request, "schoolApp/admin-expressions.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def admin_expression_detail(request, pk_expression):
    """Render the admin expression of interest details page for an admin user.

    :param request: httprequest received
    :type request: HttpRequest
    :param pk_expression: Primary Key of an expression of interest
    :type pk_expression: int
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments
    :rtype: HttpResponse
    """
    expression = Expressions.objects.get(acceptance_id=pk_expression)
    form = ExpressionForm(instance=expression)

    if request.method == "POST":
        expression.status = "Accepted"
        form = ExpressionForm(request.POST, instance=expression)
        if form.is_valid():
            form.save()

            new_booking = Booking(expression=expression, status="Pending")
            new_booking.save()

            school_email = expression.school.user.username
            send_email_expression_confirmation(school_email, expression)

            return redirect(request.path_info)

    data = {"expression": expression, "form": form}

    return render(request, "schoolApp/admin-expression-detail.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def admin_bookings(request):
    """Render the admin bookings list page for an admin user.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    bookings_list = Booking.objects.all()

    data = {"bookings": bookings_list}

    return render(request, "schoolApp/admin-bookings.html", data)

