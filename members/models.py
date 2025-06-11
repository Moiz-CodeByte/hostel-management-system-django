from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission
from django.conf import settings







class HostelOwner(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Override groups and user_permissions with unique related_name
    groups = models.ManyToManyField(
        Group,
        related_name='hostelowner_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='hostelowner_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

    
    

    

class Hostel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    total_rooms = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    





class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField()
    capacity = models.IntegerField(default=2)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.hostel.name}"








class Student(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) 
    
    
    def __str__(self):
        return self.name
    

    
    
  






class Staff(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='staff')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.role})"


class RentPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rent_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Payment of {self.amount} by {self.student.name} on {self.payment_date}"


class HostelRentPayment(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='hostel_rent_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Hostel Rent Payment of {self.amount} for {self.hostel.name} due {self.due_date}"
    




    
