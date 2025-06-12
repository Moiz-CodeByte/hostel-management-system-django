
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    create_rent, create_student, delete_payment, delete_rent, delete_staff, delete_student, edit_hostel_user, edit_rent, edit_staff, 
    edit_student, logout_view, manage_hostel_owners, edit_hostel_owner, delete_hostel_owner,
    manage_hostels, edit_hostel, delete_hostel, manage_payments, edit_payment, manage_rent,
    manage_staff, signup, login_view, create_hostel, manage_students, home, about, list_hostels_user
)


urlpatterns = [
    # Hostel Owner
    path('manage_hostel_owners/', manage_hostel_owners, name='manage_hostel_owners'),
    path('edit_hostel_owner/<int:owner_id>/', edit_hostel_owner, name='edit_hostel_owner'),
    path('delete_hostel_owner/<int:owner_id>/', delete_hostel_owner, name='delete_hostel_owner'),

    # Hostel
    path('manage_hostels/', manage_hostels, name='manage_hostels'),
    path('edit_hostel/<int:hostel_id>/', edit_hostel, name='edit_hostel'),
    path('delete_hostel/<int:hostel_id>/', delete_hostel, name='delete_hostel'),

    # Payments
    path('manage_payments/', manage_payments, name='manage_payments'),
    path('edit_payment/<int:payment_id>/', edit_payment, name='edit_payment'),
    path('delete_payment/<int:payment_id>/', delete_payment, name='delete_payment'),

    # Auth
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # fallback login
    path('create_hostel/', create_hostel, name='create_hostel'),

    # Students
    path('students/', manage_students, name='manage_students'),
    path('students/create/', create_student, name='create_student'),
    path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', delete_student, name='delete_student'),

    # Staff
    path('staff/', manage_staff, name='manage_staff'),
    path('staff/edit/<int:staff_id>/', edit_staff, name='edit_staff'),
    path('staff/delete/<int:staff_id>/', delete_staff, name='delete_staff'),


    # Rent
    path('rent/', manage_rent, name='rent_management'),
    path('rent/create/', create_rent, name='create_rent'),
    path('rent/edit/<int:rent_id>/', edit_rent, name='edit_rent'),
    path('rent/delete/<int:rent_id>/', delete_rent, name='delete_rent'),

    path('edit-hostel/<int:hostel_id>/', edit_hostel_user, name='edit_hostel_user'),
    path('my-hostel/', list_hostels_user, name='list_hostels_user'),
  
    path('logout/', logout_view, name='logout'),
    ]


