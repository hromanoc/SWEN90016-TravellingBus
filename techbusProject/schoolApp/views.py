from django.shortcuts import render

# Create your views here.
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
