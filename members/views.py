from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import HostelOwner, Hostel, Room, Student, Staff, RentPayment, HostelRentPayment
from django.db.models import Sum
from django.utils import timezone

# Hostel Owner Management
@login_required
def manage_hostel_owners(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        HostelOwner.objects.create(name=name, email=email, phone=phone, address=address)
        messages.success(request, 'Hostel Owner created successfully!')
        return redirect('manage_hostel_owners')
    
    owners = HostelOwner.objects.all()
    return render(request, 'manage_hostel_owners.html', {'owners': owners})

@login_required
def edit_hostel_owner(request, owner_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    owner = get_object_or_404(HostelOwner, id=owner_id)
    
    if request.method == 'POST':
        owner.name = request.POST.get('name')
        owner.email = request.POST.get('email')
        owner.phone = request.POST.get('phone')
        owner.address = request.POST.get('address')
        owner.save()
        
        messages.success(request, 'Hostel Owner updated successfully!')
        return redirect('manage_hostel_owners')
    
    return render(request, 'edit_hostel_owner.html', {'owner': owner})

@login_required
def delete_hostel_owner(request, owner_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    owner = get_object_or_404(HostelOwner, id=owner_id)
    owner.delete()
    
    messages.success(request, 'Hostel Owner deleted successfully!')
    return redirect('manage_hostel_owners')

# Hostel Management
@login_required
def manage_hostels(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        owner_id = request.POST.get('owner')
        total_rooms = request.POST.get('total_rooms')
        
        owner = get_object_or_404(HostelOwner, id=owner_id)
        hostel = Hostel.objects.create(name=name, location=location, owner=owner, total_rooms=total_rooms)
        
        # Create rooms based on total_rooms
        for i in range(1, int(total_rooms) + 1):
            Room.objects.create(hostel=hostel, room_number=f"Room {i}", capacity=1)
        
        messages.success(request, 'Hostel created successfully!')
        return redirect('manage_hostels')
    
    hostels = Hostel.objects.all()
    owners = HostelOwner.objects.all()
    return render(request, 'manage_hostels.html', {'hostels': hostels, 'owners': owners})

@login_required
def edit_hostel(request, hostel_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    if request.method == 'POST':
        hostel.name = request.POST.get('name')
        hostel.location = request.POST.get('location')
        owner_id = request.POST.get('owner')
        new_total_rooms = int(request.POST.get('total_rooms'))
        
        hostel.owner = get_object_or_404(HostelOwner, id=owner_id)
        
        # Handle total_rooms change
        current_total_rooms = hostel.total_rooms
        if new_total_rooms > current_total_rooms:
            # Create additional rooms
            for i in range(current_total_rooms + 1, new_total_rooms + 1):
                Room.objects.create(hostel=hostel, room_number=f"Room {i}", capacity=1)
        elif new_total_rooms < current_total_rooms:
            # Check if we can reduce rooms
            rooms_to_delete = Room.objects.filter(hostel=hostel)[new_total_rooms:]
            for room in rooms_to_delete:
                if Student.objects.filter(room=room).exists():
                    messages.error(request, f"Cannot reduce capacity. Room {room.room_number} is occupied.")
                    return render(request, 'edit_hostel.html', {'hostel': hostel, 'owners': HostelOwner.objects.all()})
            
            # Delete excess rooms
            rooms_to_delete.delete()
        
        hostel.total_rooms = new_total_rooms
        hostel.save()
        
        messages.success(request, 'Hostel updated successfully!')
        return redirect('manage_hostels')
    
    owners = HostelOwner.objects.all()
    return render(request, 'edit_hostel.html', {'hostel': hostel, 'owners': owners})

@login_required
def delete_hostel(request, hostel_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if there are students in this hostel
    if Student.objects.filter(room__hostel=hostel).exists():
        messages.error(request, "Cannot delete hostel with students. Please remove students first.")
        return redirect('manage_hostels')
    
    hostel.delete()
    messages.success(request, 'Hostel deleted successfully!')
    return redirect('manage_hostels')

# Payment Management
@login_required
def manage_payments(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    if request.method == 'POST':
        hostel_id = request.POST.get('hostel')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        
        hostel = get_object_or_404(Hostel, id=hostel_id)
        HostelRentPayment.objects.create(hostel=hostel, amount=amount, payment_date=payment_date)
        
        messages.success(request, 'Payment recorded successfully!')
        return redirect('manage_payments')
    
    payments = HostelRentPayment.objects.all().order_by('-payment_date')
    hostels = Hostel.objects.all()
    return render(request, 'manage_payments.html', {'payments': payments, 'hostels': hostels})

@login_required
def edit_payment(request, payment_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    payment = get_object_or_404(HostelRentPayment, id=payment_id)
    
    if request.method == 'POST':
        hostel_id = request.POST.get('hostel')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        
        payment.hostel = get_object_or_404(Hostel, id=hostel_id)
        payment.amount = amount
        payment.payment_date = payment_date
        payment.save()
        
        messages.success(request, 'Payment updated successfully!')
        return redirect('manage_payments')
    
    hostels = Hostel.objects.all()
    return render(request, 'edit_payment.html', {'payment': payment, 'hostels': hostels})

@login_required
def delete_payment(request, payment_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    payment = get_object_or_404(HostelRentPayment, id=payment_id)
    payment.delete()
    
    messages.success(request, 'Payment deleted successfully!')
    return redirect('manage_payments')

# Public Pages
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# Authentication
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        
        messages.success(request, 'Account created successfully!')
        return redirect('home')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'login.html')

@login_required
def create_hostel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        total_rooms = int(request.POST.get('total_rooms'))
        
        # Create hostel
        hostel = Hostel.objects.create(
            name=name,
            location=location,
            total_rooms=total_rooms,
            owner=request.user
        )
        
        # Create rooms based on total_rooms
        for i in range(1, total_rooms + 1):
            Room.objects.create(hostel=hostel, room_number=f"Room {i}", capacity=1)
        
        messages.success(request, 'Hostel created successfully!')
        return redirect('list_hostels_user')
    
    return render(request, 'create_hostel.html')

# Student Management
@login_required
def manage_students(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    students = Student.objects.filter(room__hostel=hostel)
    rooms = Room.objects.filter(hostel=hostel)
    
    # Get available rooms (not full)
    available_rooms = [room for room in rooms if room.students.count() < room.capacity]
    
    return render(request, 'index.html', {
        'students': students,
        'hostel': hostel,
        'available_rooms': available_rooms
    })

@login_required
def create_student(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        room_id = request.POST.get('room')
        
        # Check if email is unique
        if Student.objects.filter(email=email).exists():
            messages.error(request, "A student with this email already exists!")
            return redirect('manage_students', hostel_id=hostel.id)
        
        room = get_object_or_404(Room, id=room_id)
        
        # Check if room is full
        if room.students.count() >= room.capacity:
            messages.error(request, "This room is already full!")
            return redirect('manage_students', hostel_id=hostel.id)
        
        Student.objects.create(name=name, email=email, phone=phone, room=room)
        messages.success(request, 'Student added successfully!')
        return redirect('manage_students', hostel_id=hostel.id)
    
    rooms = Room.objects.filter(hostel=hostel)
    available_rooms = [room for room in rooms if room.students.count() < room.capacity]
    
    return render(request, 'create_student.html', {
        'hostel': hostel,
        'available_rooms': available_rooms
    })

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    hostel = student.room.hostel
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        room_id = request.POST.get('room')
        
        # Check if email is unique (excluding this student)
        if Student.objects.filter(email=email).exclude(id=student_id).exists():
            messages.error(request, "A student with this email already exists!")
            return redirect('edit_student', student_id=student.id)
        
        room = get_object_or_404(Room, id=room_id)
        
        # Check if room is full (excluding this student)
        if room.id != student.room.id and room.students.count() >= room.capacity:
            messages.error(request, "This room is already full!")
            return redirect('edit_student', student_id=student.id)
        
        student.name = name
        student.email = email
        student.phone = phone
        student.room = room
        student.save()
        
        messages.success(request, 'Student updated successfully!')
        return redirect('manage_students', hostel_id=hostel.id)
    
    rooms = Room.objects.filter(hostel=hostel)
    available_rooms = [room for room in rooms if room.students.count() < room.capacity or room.id == student.room.id]
    
    return render(request, 'edit_student.html', {
        'student': student,
        'hostel': hostel,
        'available_rooms': available_rooms
    })

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    hostel = student.room.hostel
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.user != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('manage_students', hostel_id=hostel.id)

# Staff Management
@login_required
def manage_staff(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    staff = Staff.objects.filter(hostel=hostel)
    return render(request, 'staff_management.html', {'staff': staff, 'hostel': hostel})

@login_required
def create_staff(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        
        Staff.objects.create(name=name, position=position, phone=phone, salary=salary, hostel=hostel)
        messages.success(request, 'Staff member added successfully!')
        return redirect('manage_staff', hostel_id=hostel.id)
    
    return render(request, 'create_staff.html', {'hostel': hostel})

@login_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    hostel = staff.hostel
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        
        staff.name = name
        staff.position = position
        staff.phone = phone
        staff.salary = salary
        staff.save()
        
        messages.success(request, 'Staff member updated successfully!')
        return redirect('manage_staff', hostel_id=hostel.id)
    
    return render(request, 'edit_staff.html', {'staff': staff, 'hostel': hostel})

@login_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    hostel = staff.hostel
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    staff.delete()
    messages.success(request, 'Staff member deleted successfully!')
    return redirect('manage_staff', hostel_id=hostel.id)

# Rent Management
@login_required
def manage_rent(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    rent_payments = RentPayment.objects.filter(student__room__hostel=hostel).order_by('-due_date')
    students = Student.objects.filter(room__hostel=hostel)
    
    return render(request, 'rent_management.html', {
        'rent_payments': rent_payments,
        'students': students,
        'hostel': hostel
    })

@login_required
def create_rent(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date')
        is_paid = request.POST.get('is_paid') == 'True'
        payment_date = request.POST.get('payment_date') if is_paid else None
        
        student = get_object_or_404(Student, id=student_id)
        
        # Verify student belongs to this hostel
        if student.room.hostel.id != hostel.id:
            messages.error(request, "Invalid student selection!")
            return redirect('manage_rent', hostel_id=hostel.id)
        
        RentPayment.objects.create(
            student=student,
            amount=amount,
            due_date=due_date,
            is_paid=is_paid,
            payment_date=payment_date
        )
        
        messages.success(request, 'Rent payment recorded successfully!')
        return redirect('manage_rent', hostel_id=hostel.id)
    
    return redirect('manage_rent', hostel_id=hostel.id)

@login_required
def edit_rent(request, rent_id):
    rent = get_object_or_404(RentPayment, id=rent_id)
    hostel = rent.student.room.hostel
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date')
        is_paid = request.POST.get('is_paid') == 'True'
        payment_date = request.POST.get('payment_date') if is_paid else None
        
        student = get_object_or_404(Student, id=student_id)
        
        # Verify student belongs to this hostel
        if student.room.hostel.id != hostel.id:
            messages.error(request, "Invalid student selection!")
            return redirect('edit_rent', rent_id=rent.id)
        
        rent.student = student
        rent.amount = amount
        rent.due_date = due_date
        rent.is_paid = is_paid
        rent.payment_date = payment_date
        rent.save()
        
        messages.success(request, 'Rent payment updated successfully!')
        return redirect('manage_rent', hostel_id=hostel.id)
    
    students = Student.objects.filter(room__hostel=hostel)
    return render(request, 'edit_rent.html', {
        'rent': rent,
        'students': students,
        'hostel': hostel
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('home')
    
    return render(request, 'edit_profile.html')

@login_required
def edit_hostel_user(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    # Check if user is authorized to manage this hostel
    if hostel.owner != request.user:
        messages.error(request, "You don't have permission to edit this hostel.")
        return redirect('home')
    
    if request.method == 'POST':
        hostel.name = request.POST.get('name')
        hostel.location = request.POST.get('location')
        new_total_rooms = int(request.POST.get('total_rooms'))
        
        # Handle total_rooms change
        current_total_rooms = hostel.total_rooms
        if new_total_rooms > current_total_rooms:
            # Create additional rooms
            for i in range(current_total_rooms + 1, new_total_rooms + 1):
                Room.objects.create(hostel=hostel, room_number=f"Room {i}", capacity=1)
        elif new_total_rooms < current_total_rooms:
            # Check if we can reduce rooms
            rooms_to_delete = Room.objects.filter(hostel=hostel)[new_total_rooms:]
            for room in rooms_to_delete:
                if Student.objects.filter(room=room).exists():
                    messages.error(request, f"Cannot reduce capacity. Room {room.room_number} is occupied.")
                    return render(request, 'edit_hostel_user.html', {'hostel': hostel})
            
            # Delete excess rooms
            rooms_to_delete.delete()
        
        hostel.capacity = new_capacity
        hostel.save()
        
        messages.success(request, 'Hostel updated successfully!')
        return redirect('list_hostels_user')
    
    return render(request, 'edit_hostel_user.html', {'hostel': hostel})

@login_required
def delete_rent(request, rent_id):
    rent = get_object_or_404(RentPayment, id=rent_id)
    hostel = rent.student.room.hostel
    
    # Check if user is authorized to manage this hostel
    if not request.user.is_superuser and hostel.owner != request.user:
        messages.error(request, "You don't have permission to access this hostel.")
        return redirect('home')
    
    rent.delete()
    messages.success(request, 'Rent payment deleted successfully!')
    return redirect('manage_rent', hostel_id=hostel.id)

@login_required
def list_hostels_user(request):
    hostels = Hostel.objects.filter(owner=request.user)
    return render(request, 'list_hostels_user.html', {'hostels': hostels})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')
