from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, Expressions


class DateInput(forms.DateInput):
    input_type = "date"


class ExpressionForm(ModelForm):
    class Meta:
        model = Expressions
        fields = ["suggested_start_date", "suggested_end_date"]
        widgets = {
            "suggested_start_date": DateInput(),
            "suggested_end_date": DateInput(),
        }


class BookingForm(ModelForm):
    SPECIAL_OPTIONS = (
        ("True", "Yes"),
        ("False", "No"),
    )

    total_students = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-sm",
                "oninput": "myFunction()",
                "min": 1,
                "max": 10,
            }
        ),
        required=False,
    )
    total_cost = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control form-control-sm", "readonly": "True"}
        ),
        required=False,
    )

    special_activity = forms.ChoiceField(
        choices=SPECIAL_OPTIONS,
        widget=forms.Select(
            attrs={"class": "form-select", "onchange": "EnableDisableTextBox(this)"}
        ),
    )

    class Meta:
        model = Booking
        fields = [
            "start_date",
            "end_date",
            "special_activity",
            "total_students",
            "total_cost",
        ]
        widgets = {
            "start_date": DateInput(),
            "end_date": DateInput(),
        }


class CreateExpressionForm(ModelForm):

    SCHOOL_TYPE = (
        ("Hosting School", "Hosting School"),
        ("Visiting School", "Visiting School"),
    )

    PARKING_PRESENT = (
        ("true", "Yes"),
        ("false", "No"),
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "maxlength": 250})
    )
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    state = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    postal_code = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10})
    )
    school_type = forms.ChoiceField(
        choices=SCHOOL_TYPE,
        widget=forms.Select(
            attrs={"class": "form-select", "onchange": "EnableDisableTextBox(this)"}
        ),
    )
    # parking_present = forms.ChoiceField(
    #     choices=PARKING_PRESENT, widget=forms.Select(attrs={"class": "form-select"})
    # )
    total_spaces = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 100}),
        required=False,
    )
    total_areas = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
        required=False,
    )
    visiting_school_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "maxlength": 50}),
        required=False,
    )
    nearest_school_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "maxlength": 50}),
        required=False,
    )
    distance_nearest_school = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 20}),
        required=False,
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": "3", "maxlength": "250"}
        )
    )

    class Meta:
        model = Expressions
        fields = [
            "school",
            "address",
            "city",
            "state",
            "postal_code",
            "school_type",
            "parking_present",
            "total_spaces",
            "total_areas",
            "visiting_school_name",
            "nearest_school_name",
            "distance_nearest_school",
            "message",
        ]


class CreateScoolForm(UserCreationForm):

    username = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
        ]
