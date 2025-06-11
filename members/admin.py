from django.contrib import admin
from .models import HostelOwner, Hostel, HostelRentPayment, Student, Staff, RentPayment


@admin.register(HostelOwner)
class HostelOwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_active')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('is_active',)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_rooms', 'is_active', 'owner')
    search_fields = ('name', 'owner__name')
    list_filter = ('is_active', 'owner')


@admin.register(HostelRentPayment)
class HostelRentPaymentAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'amount', 'due_date', 'payment_date', 'is_paid')
    search_fields = ('hostel__name',)
    list_filter = ('is_paid', 'due_date')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'hostel', 'room', 'is_active')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('is_active', 'hostel', 'room')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'role', 'hostel', 'is_active')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('is_active', 'role', 'hostel')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RentPayment)
class StudentRentPaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_date', 'is_paid')
    search_fields = ('student__name', 'student__email', 'student__hostel__name')
    list_filter = ('is_paid', 'student__hostel')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
