from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class School(models.Model):
    """
    Represents a school
    """
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=50, null=True)
    contact_name = models.CharField(max_length=50, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """
        String representation of a school staff member
        """
        return self.user.username


class Expressions(models.Model):
    """
    Represents an Expression of Interest
    """

    SCHOOL_TYPE = (
        ("Hosting School", "Hosting School"),
        ("Visiting School", "Visiting School"),
    )

    STATUS = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted")
    )

    acceptance_id = models.AutoField(primary_key=True, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    postal_code = models.PositiveIntegerField(null=True)
    school_type = models.CharField(max_length=50, null=True, choices=SCHOOL_TYPE)
    parking_present = models.BooleanField(null=True, default=False)
    total_spaces = models.PositiveIntegerField(null=True)
    total_areas = models.PositiveIntegerField(null=True)
    visiting_school_name = models.CharField(max_length=50, null=True)
    nearest_school_name = models.CharField(max_length=50, null=True)
    distance_nearest_school = models.PositiveIntegerField(null=True)
    message = models.CharField(max_length=250, null=True)
    status = models.CharField(
        max_length=15, null=True, choices=STATUS, default="Pending"
    )
    suggested_start_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    suggested_end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """
        String representation of an Expression of Interest
        """
        return f"Acceptence ID: {self.acceptance_id}. School Name: {self.school.school_name}"

class Booking(models.Model):
    """
    Represents a Booked service
    """

    STATUS = (
        ("Reserved", "Reserved"),
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled"),
    )

    SERVICE_COST_PER_PERSON = 30

    expression = models.ForeignKey(Expressions, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    special_activity = models.BooleanField(null=True, default=False)
    total_students = models.PositiveIntegerField(null=True, default=0)
    cost_per_person = models.PositiveIntegerField(null=True, default=SERVICE_COST_PER_PERSON)
    total_cost = models.PositiveIntegerField(null=True, default=0)
    status = models.CharField(
        max_length=15, null=True, choices=STATUS, default="Pending"
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    reason_cancellation = models.CharField(
        max_length=250, null=True, default="No reason provided"
    )

    def __str__(self):
        """
        String representation of a Booked service
        """
        return f"Acceptence ID: {self.expression.acceptance_id}. School Name: {self.expression.school.school_name}. Total Cost: {self.total_cost}"
