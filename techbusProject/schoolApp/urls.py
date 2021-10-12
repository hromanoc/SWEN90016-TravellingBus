from django.urls import path
from . import views

urlpatterns = [
    path("", views.school_login, name="login"),
    path("register/", views.school_register, name="register"),
    path("login/", views.school_login, name="login"),
    path("logout/", views.school_logout, name="logout"),

    path("admin-dashboard/", views.admin_dashboard, name="admin-dashboard"),
    path("admin-expressions/", views.admin_expressions, name="admin-expressions"),
    path("admin-bookings/", views.admin_bookings,name="admin-bookings" ),
    path("admin-expression-detail/<str:pk_expression>/", views.admin_expression_detail, name="admin-expression-detail"),


    path("school-dashboard/", views.school_home, name="school-dashboard"),
    path("school-expressions/", views.school_expressions, name="school-expressions"),
    path("school-create-expression/<str:pk_school>", views.school_create_expression, name="school-create-expression"),
    path("school-expression-detail/<str:pk_expression>/", views.school_expression_detail, name="school-expression-detail"),
    path("school-bookings/", views.school_bookings,name="school-bookings" ),
    path("school-booking-detail/<str:pk_booking>", views.school_booking_detail,name="school-booking-detail" ),

    path("school-booking-cancel/<str:pk_booking>/", views.school_booking_cancel, name="school-booking-cancel"),
]
