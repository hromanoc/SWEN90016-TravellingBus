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

from .date_search import *
from datetime import date, datetime

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
        
        form = ExpressionForm(request.POST, instance=expression)
        expression.status = "Accepted"
        
        date_list = get_taken_expression_dates() ## get dates already scheduled
        date_list.sort() #sort these
        s_date = datetime.strptime(form['suggested_start_date'].value(), "%Y-%m-%d").date() # define start date
        e_date = datetime.strptime(form['suggested_end_date'].value(), "%Y-%m-%d").date() # define end date
        dates = date_between(s_date, e_date) # get dates between start and end date
        is_taken = binary_search_dates(dates, date_list) # see if dates already taken

        if form.is_valid() and not is_taken:

            form.save()
            new_booking = Booking(expression=expression, status="Pending")
            new_booking.save()

            school_email = expression.school.user.username
            send_email_expression_confirmation(school_email, expression)

            return redirect(request.path_info)
        elif is_taken:
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

#####################
# School's Views
#####################


@unauthenticated_user
def school_register(request):
    """Render the school registration page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    form = CreateScoolForm()

    if request.method == "POST":
        form = CreateScoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            school_name = request.POST["school_name"]
            contact_name = request.POST["contact_name"]
            contact_number = request.POST["contact_number"]

            group = Group.objects.get(name="school")
            school.groups.add(group)
            School.objects.create(
                user=school,
                school_name=school_name,
                contact_name=contact_name,
                contact_number=contact_number,
            )

            messages.success(request, f"Account was created for {school_name}")
            return redirect("login")

    data = {"form": form}

    return render(request, "schoolApp/school-registration.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["school"])
def school_home(request):
    """Render the school home page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    school_id = request.user.school.id
    expressions = request.user.school.expressions_set.all()
    if expressions:
        bookings = [
            expression.booking_set.all()[0]
            for expression in expressions
            if expression.booking_set.all()
        ]
    else:
        bookings = []

    data = {"expressions": expressions,
            "bookings": bookings, "school_id": school_id}

    return render(request, "schoolApp/school-dashboard.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["school"])
def school_expressions(request):
    """Render the school expression of interests list page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    school_id = request.user.school.id
    expressions = request.user.school.expressions_set.all()

    data = {"expressions": expressions, "school_id": school_id}

    return render(request, "schoolApp/school-expressions.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["school"])
def school_create_expression(request, pk_school):
    """Render the school expression of interest create page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :param pk_school: Primary Key of a School
    :type pk_school: int
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    school = School.objects.get(id=pk_school)
    form = CreateExpressionForm(initial={"school": school})

    if request.method == "POST":
        form = CreateExpressionForm(request.POST)
       


        if form.is_valid():
            expression = form.save()
            messages.success(
                request, f"Expression was created for {expression.school.school_name}"
            )
            admin_email = ADMIN_EMAIL
            send_email_expression(admin_email, expression)

            return redirect("school-dashboard")

    data = {"form": form, "school": school}

    return render(request, "schoolApp/school-create-expression.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["school"])
def school_expression_detail(request, pk_expression):
    """Render the school expression of interest detail page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :param pk_expression: Primary Key of an expression of interest
    :type pk_expression: int
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    expression = Expressions.objects.get(acceptance_id=pk_expression)
    form = ExpressionForm(instance=expression)

    if request.method == "POST":
        expression.status = "Accepted"
        form = ExpressionForm(request.POST, instance=expression)
        if form.is_valid():
            form.save()

            return redirect(request.path_info)

    data = {"expression": expression, "form": form}

    return render(request, "schoolApp/school-expression-detail.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["school"])
def school_bookings(request):
    """Render the school bookings list page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    school_id = request.user.school.id
    expressions = request.user.school.expressions_set.all()
    if expressions:
        bookings = [
            expression.booking_set.all()[0]
            for expression in expressions
            if expression.booking_set.all()
        ]
    else:
        bookings = []

    data = {"school_id": school_id, "bookings": bookings}

    return render(request, "schoolApp/school-bookings.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["school"])
def school_booking_detail(request, pk_booking):
    """Render the school booking detail page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :param pk_booking: Primary Key of a Booking
    :type pk_booking: int
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    booking = Booking.objects.get(id=pk_booking)
    expression = booking.expression
    form = BookingForm(instance=booking)

    if request.method == "POST":
        booking.status = "Reserved"
        if request.POST["special_activity"] == "True":
            expression.special_activity = True
        else:
            expression.special_activity = False

        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()

            return redirect(request.path_info)

    data = {"booking": booking, "expression": expression, "form": form}

    return render(request, "schoolApp/school-booking-detail.html", data)


@login_required(login_url="login")
@allowed_users(allowed_roles=["school"])
def school_booking_cancel(request, pk_booking):
    """Render the school booking cancel page for a school representative.

    :param request: httprequest received
    :type request: HttpRequest
    :param pk_booking: Primary Key of a Booking
    :type pk_booking: int
    :return: Return a HttpResponse whose content is filled with the result of the passed arguments.
    :rtype: HttpResponse
    """
    booking = Booking.objects.get(id=pk_booking)

    if request.method == "POST":
        booking.status = "Cancelled"
        booking.reason_cancellation = request.POST["reason_cancellation"]
        booking.save()

        admin_email = ADMIN_EMAIL
        send_email_booking_cancellation(admin_email, booking)

        return redirect("school-dashboard")

    data = {"booking": booking}
    return render(request, "schoolApp/school-booking-cancel.html", data)
