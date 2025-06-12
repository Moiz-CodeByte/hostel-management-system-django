from django.shortcuts import render, redirect, get_object_or_404
from .models import   Hostel , HostelRentPayment , HostelOwner, RentPayment, Staff ,Student, Hostel, Room
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q , Count




@require_http_methods(["GET", "POST"])
def manage_hostel_owners(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        is_active_str = request.POST.get('is_active')
        is_active = True if is_active_str == 'True' else False

        HostelOwner.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            is_active=is_active
        )
        return redirect('manage_hostel_owners') 

    hostel_owners = HostelOwner.objects.all().order_by('id')
    context = {
        'hostel_owners': hostel_owners,
    }
    return render(request, 'manage_hostel_owners.html', context)



def edit_hostel_owner(request, owner_id):
    owner = get_object_or_404(HostelOwner, pk=owner_id)
    if request.method == 'POST':
        owner.name = request.POST.get('name')
        owner.email = request.POST.get('email')
        owner.phone_number = request.POST.get('phone_number')
        owner.address = request.POST.get('address')
        is_active_str = request.POST.get('is_active')
        owner.is_active = True if is_active_str == 'True' else False
        owner.save()
        return redirect('manage_hostel_owners')  

    context = {
        'owner': owner,
    }
    return render(request, 'edit_hostel_owner.html', context)




def delete_hostel_owner(request, owner_id):
    owner = get_object_or_404(HostelOwner, pk=owner_id)
    if request.method == "POST":
        owner.delete()
        return redirect('manage_hostel_owners') 

    context = {
        'owner': owner,
    }
    return render(request, 'delete_hostel_owner.html', context)




def get_hostel_owners(request):
    hostel_owners = HostelOwner.objects.all()
    context = {
        'hostel_owners': hostel_owners,
    }
    return render(request, 'manage_hostel_owners.html', context)









@require_http_methods(["GET", "POST"])
def manage_hostels(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        total_rooms = request.POST.get('total_rooms')
        is_active_str = request.POST.get('is_active')
        is_active = True if is_active_str == 'True' else False
        owner_id = request.POST.get('owner')  
       
        Hostel.objects.create(
            name=name,
            location=location,
            total_rooms=total_rooms,
            is_active=is_active,
            owner_id=owner_id  
        )
        return redirect('manage_hostels')
    
    hostels = Hostel.objects.all().order_by('id')
    hostel_owners = HostelOwner.objects.all() 
    context = {
        'hostels': hostels,
        'hostel_owners': hostel_owners
    }
    return render(request, 'manage_hostels.html', context)






def edit_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    if request.method == 'POST':
        hostel.name = request.POST.get('name')
        hostel.location = request.POST.get('location')
        hostel.total_rooms = request.POST.get('total_rooms')
        hostel.is_active = request.POST.get('is_active') == 'True'
        hostel.owner_id = request.POST.get('owner') 
        hostel.save()
        return redirect('manage_hostels')
    hostel_owners = HostelOwner.objects.all() 
    context = {
        'hostel': hostel,
        'hostel_owners': hostel_owners,
    }
    return render(request, 'edit_hostel.html', context)



 

def delete_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    if request.method == "POST":
        hostel.delete()
        return redirect('manage_hostels')  
    context = {
        'hostel': hostel,
    }
    return render(request, 'delete_hostel.html', context)




@require_http_methods(["GET", "POST"])
def manage_payments(request):

    if request.method == 'POST':
        hostel_id = request.POST.get('hostel')
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date')
        payment_date = request.POST.get('payment_date')
        is_paid = request.POST.get('is_paid') == 'True'
        
        HostelRentPayment.objects.create(
            hostel_id=hostel_id,
            amount=amount,
            due_date=due_date,
            payment_date=payment_date,
            is_paid=is_paid
        )
        return redirect('manage_payments')
    
    payments = HostelRentPayment.objects.all().order_by('due_date')
    hostels = Hostel.objects.all()  
    context = {
        'payments': payments,
        'hostels': hostels
    }
    return render(request, 'manage_payments.html', context)


def edit_payment(request, payment_id):
    payment = get_object_or_404( HostelRentPayment, pk=payment_id)
    if request.method == 'POST':
        payment.amount = request.POST.get('amount')
        payment.date = request.POST.get('date')
        payment.hostel_id = request.POST.get('hostel')  
        payment.save()
        return redirect(reverse('manage_payments'))
    
    hostels = Hostel.objects.all() 
    context = {
        'payment': payment,
        'hostels': hostels,
    }
    return render(request, 'edit_payments.html', context)



def delete_payment(request, payment_id):
    payment = get_object_or_404(HostelRentPayment, pk=payment_id)
    if request.method == "POST":
        payment.delete()
        return redirect('manage_payments')  
    context = {
        'payment': payment,
    }
    return render(request, 'delete_payment.html', context)










def home(request): 
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')




def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if HostelOwner.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        if HostelOwner.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        # Create new user with empty phone and address
        owner = HostelOwner(username=username, email=email, phone_number='', address='')
        owner.set_password(password)
        owner.save()
        
        # Log the user in automatically
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Account created successfully. Please create your hostel and complete your profile.')
            return redirect('create_hostel')
        else:
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')

    return render(request, 'signup.html')






def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            
            # Check if user has completed their profile
            if not (user.phone_number and user.address):
                messages.info(request, "Please complete your profile information.")
                # Get the first hostel or redirect to create one
                hostel = Hostel.objects.filter(owner=user).first()
                if hostel:
                    return redirect('edit_hostel_user', hostel_id=hostel.id)
                else:
                    return redirect('create_hostel')
            
            return redirect('list_hostels_user')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')




@login_required
def create_hostel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        total_rooms = int(request.POST.get('total_rooms'))
        is_active = request.POST.get('is_active') == 'True'

        hostel = Hostel.objects.create(
            owner=request.user,
            name=name,
            location=location,
            total_rooms=total_rooms,  
            is_active=is_active
        )

        for i in range(1, total_rooms + 1):
            Room.objects.create(
               hostel=hostel,
               room_number=i,
               capacity=2,
               monthly_price=0,
               is_available=True
        )

        messages.success(request, 'Hostel created successfully!')
        
        # Always redirect to edit hostel to ensure contact information is complete
        messages.info(request, 'Please complete your profile information.')
        return redirect('edit_hostel_user', hostel_id=hostel.id)

    return render(request, 'create_hostel.html')










@login_required
def manage_students(request):
    hostel = Hostel.objects.filter(owner=request.user).first()
    students = Student.objects.filter(hostel=hostel)

    query = request.GET.get('search')
    if query:
        students = students.filter(name__icontains=query) | students.filter(email__icontains=query)

    status = request.GET.get('status')
    if status == 'active':
        students = students.filter(is_active=True)
    elif status == 'inactive':
        students = students.filter(is_active=False)

    return render(request, 'index.html', {
        'students': students,
        'query': query
    })






@login_required
def create_student(request):
    hostel = Hostel.objects.filter(owner=request.user).first()

    rooms = Room.objects.filter(hostel=hostel).annotate(
        student_count=Count('students')
    )

    # Add a custom attribute to each room: remaining_capacity
    for room in rooms:
        room.remaining_capacity = room.capacity - room.student_count

    if request.method == 'POST':
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        department = request.POST.get('department')
        room_id = request.POST.get('room')
        registration_date = request.POST.get('registration_date')
        is_active = request.POST.get('is_active') == 'True'

        selected_room = Room.objects.filter(id=room_id, hostel=hostel).first()

        if selected_room and selected_room.students.count() >= selected_room.capacity:
            messages.error(request, 'Selected room is full.')
            return render(request, 'create_student.html', {'rooms': rooms})

    
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'A student with this email already exists.')
            return render(request, 'create_student.html', {'rooms': rooms})

        # Create student with new fields
        student = Student.objects.create(
            hostel=hostel,
            name=name,
            father_name=father_name,
            email=email,
            phone_number=phone_number,
            address=address,
            department=department,
            room=selected_room,
            is_active=is_active
        )
        
        # Set registration date if provided
        if registration_date:
            student.registration_date = registration_date
            student.save()
        messages.success(request, 'Student created successfully!')
        return redirect('manage_students')

    return render(request, 'create_student.html', {'rooms': rooms})







@login_required
def edit_student(request, student_id):
    hostel = Hostel.objects.filter(owner=request.user).first()
    student = get_object_or_404(Student, id=student_id, hostel=hostel)
    rooms = Room.objects.filter(hostel=hostel)

    if request.method == 'POST':
        room_id = request.POST.get('room')
        selected_room = Room.objects.filter(id=room_id, hostel=hostel).first() if room_id else None

        # If room changed and new room is full
        if selected_room and selected_room != student.room and selected_room.students.count() >= selected_room.capacity:
            messages.error(request, 'Selected room is full.')
            return render(request, 'edit_student.html', {'student': student, 'rooms': rooms})

        student.name = request.POST.get('name')
        student.father_name = request.POST.get('father_name')
        student.email = request.POST.get('email')
        student.phone_number = request.POST.get('phone_number')
        student.address = request.POST.get('address')
        student.department = request.POST.get('department')
        student.room = selected_room
        student.is_active = request.POST.get('is_active') == 'True'
        
        # Update registration date if provided
        registration_date = request.POST.get('registration_date')
        if registration_date:
            student.registration_date = registration_date
            
        student.save()

        messages.success(request, 'Student updated successfully!')
        return redirect('manage_students')

    return render(request, 'edit_student.html', {'student': student, 'rooms': rooms})


@login_required
def delete_student(request, student_id):
    hostel = Hostel.objects.filter(owner=request.user).first()
    student = get_object_or_404(Student, id=student_id, hostel=hostel)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('manage_students')

    return render(request, 'delete_student.html', {'student': student})











@login_required
def manage_staff(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    staff_members = Staff.objects.filter(hostel__owner=request.user)

    if search_query:
        staff_members = staff_members.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(role__icontains=search_query)
        )

    if status_filter == 'active':
        staff_members = staff_members.filter(is_active=True)
    elif status_filter == 'inactive':
        staff_members = staff_members.filter(is_active=False)

    if request.method == 'POST':
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        salary = request.POST.get('salary')
        is_active = request.POST.get('is_active') == 'True'

        Staff.objects.create(
            hostel=request.user.hostel_set.first(),
            name=name,
            father_name=father_name,
            role=role,
            phone_number=phone_number,
            email=email,
            address=address,
            salary=salary if salary else None,
            is_active=is_active
        )
        messages.success(request, 'Staff member added successfully!')
        return redirect('manage_staff')

    return render(request, 'manage_staff.html', {
        'staff_members': staff_members,
        'search_query': search_query,
        'status_filter': status_filter
    })




@login_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id, hostel__owner=request.user)

    if request.method == 'POST':
        staff.name = request.POST.get('name')
        staff.father_name = request.POST.get('father_name')
        staff.role = request.POST.get('role')
        staff.phone_number = request.POST.get('phone_number')
        staff.email = request.POST.get('email')
        staff.address = request.POST.get('address')
        staff.salary = request.POST.get('salary') if request.POST.get('salary') else None
        staff.is_active = request.POST.get('is_active') == 'True'
        staff.save()
        messages.success(request, 'Staff member updated successfully!')
        return redirect('manage_staff')

    return render(request, 'edit_staff.html', {'staff': staff})





@login_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id, hostel__owner=request.user)

    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Staff member deleted.')
        return redirect('manage_staff')

    return render(request, 'delete_staff.html', {'staff': staff})




@login_required
def manage_rent(request):
    students = Student.objects.filter(hostel__owner=request.user)
    rent_payments = RentPayment.objects.filter(student__hostel__owner=request.user).order_by('-payment_date')
    return render(request, 'rent_management.html', {'students': students, 'rent_payments': rent_payments})

@login_required
def create_rent(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        amount = request.POST.get('amount')
        is_paid = request.POST.get('is_paid') == 'True'
        student = get_object_or_404(Student, id=student_id, hostel__owner=request.user)

        RentPayment.objects.create(student=student, amount=amount, is_paid=is_paid)
        messages.success(request, 'Rent payment added.')
    return redirect('rent_management')

@login_required
def edit_rent(request, rent_id):
    rent = get_object_or_404(RentPayment, id=rent_id, student__hostel__owner=request.user)
    if request.method == 'POST':
        rent.amount = request.POST.get('amount')
        rent.is_paid = request.POST.get('is_paid') == 'True'
        rent.save()
        messages.success(request, 'Rent payment updated.')
        return redirect('rent_management')
    
    
    return render(request, 'edit_rent.html', {'rent': rent})




@login_required
def edit_hostel_user(request, hostel_id=None):
    # If hostel_id is provided, get that specific hostel
    # Otherwise, get the first hostel of this owner
    if hostel_id:
        hostel = get_object_or_404(Hostel, id=hostel_id, owner=request.user)
    else:
        hostels = Hostel.objects.filter(owner=request.user).order_by('id')
        if not hostels.exists():
            messages.error(request, "You don't have any hostels to edit.")
            return redirect('create_hostel')
        hostel = hostels.first()

    # Check if user has completed their profile
    user_profile_complete = bool(request.user.phone_number and request.user.address)
    
    if request.method == 'POST':
        # Get hostel data
        name = request.POST.get('name')
        location = request.POST.get('location')
        total_rooms_str = request.POST.get('total_rooms')
        is_active = request.POST.get('is_active') == 'True'
        
        # Get user profile data
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        # Validate required fields
        if not (name and location and total_rooms_str and phone_number and address):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'edit_hostel_user.html', {
                'hostel': hostel,
                'user_profile_complete': user_profile_complete
            })

        try:
            total_rooms = int(total_rooms_str)
            if total_rooms < 1:
                raise ValueError
        except ValueError:
            messages.error(request, "Total rooms must be a positive number.")
            return render(request, 'edit_hostel_user.html', {
                'hostel': hostel,
                'user_profile_complete': user_profile_complete
            })

        old_total = hostel.total_rooms

        # Update hostel details
        hostel.name = name
        hostel.location = location
        hostel.is_active = is_active
        hostel.total_rooms = total_rooms
        hostel.save()
        
        # Update user profile details
        request.user.phone_number = phone_number
        request.user.address = address
        request.user.save()

        if total_rooms > old_total:
            for i in range(old_total + 1, total_rooms + 1):
                Room.objects.create(
                    hostel=hostel,
                    room_number=i,
                    capacity=2,
                    monthly_price=0,
                    is_available=True
                )
        elif total_rooms < old_total:
            messages.warning(request, "Reducing total rooms does not delete existing rooms automatically.")

        messages.success(request, "Hostel and profile updated successfully!")
        return redirect('list_hostels_user')

    return render(request, 'edit_hostel_user.html', {
        'hostel': hostel,
        'user_profile_complete': user_profile_complete
    })


@login_required
def delete_rent(request, rent_id):
    rent = get_object_or_404(RentPayment, id=rent_id, student__hostel__owner=request.user)
    rent.delete()
    messages.success(request, 'Rent payment deleted.')
    return redirect('rent_management')


@login_required
def list_hostels_user(request):
    hostels = Hostel.objects.filter(owner=request.user)
    
    # If user has only one hostel, redirect directly to edit page
    if hostels.count() == 1:
        return redirect('edit_hostel_user', hostel_id=hostels.first().id)
    
    return render(request, 'list_hostels_user.html', {'hostels': hostels})


def logout_view(request):
    logout(request)
    return redirect('home')
