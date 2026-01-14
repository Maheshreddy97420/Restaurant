from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
# Create your views here.
def home(request):
    return render(request,'home.html')

@login_required(login_url='login_')
def user_home(request):
    if request.user.is_staff:
        return render(request, '403.html')
    return render(request,'user_home.html')

@staff_member_required
def admin_home(request):
    total_reservations = Reservation.objects.count()
    today_reservations = Reservation.objects.filter(
        reservation_date=now().date()
    ).count()
    total_tables = Table.objects.count()

    context = {
        'total_reservations': total_reservations,
        'today_reservations': today_reservations,
        'total_tables': total_tables,
    }

    return render(request, 'admin_home.html', context)

@login_required(login_url='login_')
def reservation(request):
    if request.user.is_staff:
        return render(request,'403.html')
    if request.method == 'POST':
        date=request.POST['date']
        time=request.POST['time']
        guests=int(request.POST['guests'])
        table=Table.objects.filter(capacity__gte=guests).first()

        if not table:
            return render(request,'reservation.html',{'error':'No Table Available'})
        
        existing=Reservation.objects.filter(
            table=table,
            reservation_date=date,
            time_slot=time
        ).exists()
        
        if existing:
            return render(request,'reservation.html',{'msg':'Table Already booked'})
        
        Reservation.objects.create(
            user=request.user,
            table=table,
            reservation_date=date,
            time_slot=time,
            guests=guests
        )
        return render(request,'reservation.html',{'data':'Booking Succesfull..!!'})
    return render(request,'reservation.html')

@login_required(login_url='login_')
def reserved(request):
    if request.user.is_staff:
        return render(request,'403.html')
    
    data=Reservation.objects.filter(user=request.user)
    if not data:
        return render(request,'reserved.html',{'msg':'Reservations are Empty..!!'})
    return render(request,'reserved.html',{'data':data})

@login_required(login_url='login_')
def cancle(request,pk):
    Reservation.objects.filter(id=pk,user=request.user).delete()
    return redirect('reserved')

@staff_member_required(login_url='login_')
def view_reservations(request):
    data=Reservation.objects.all().order_by('reservation_date','time_slot')
    return render(request,'view_reservations.html',{'data':data})

@staff_member_required(login_url='login_')
def date_reservation(request):
    date=request.GET.get('date')
    data=Reservation.objects.all()
    if date:
        data=data.filter(reservation_date=date)
    return render(request,'date_reservation.html',{'data':data})

@staff_member_required(login_url='login_')
def admin_cancle(request,pk):
    Reservation.objects.filter(id=pk).delete()
    return redirect('view_reservations')

@staff_member_required(login_url='login_')
def admin_modify(request,pk):
    reservation=Reservation.objects.get(id=pk)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = int(request.POST.get('guests'))
        table=Table.objects.filter(capacity__gte=guests).first()
        if not table:
            return render(request,'admin_modify.html',{'msg':'No table available for given guest count','reservation':reservation})
        conflict=Reservation.objects.filter(table=table,
                                            reservation_date=date,
                                            time_slot=time).exclude(id=pk).exists()
        if conflict:
            return render(request,'admin_modify.html',{'error':'Table Already booked for the time slot.','reservation':reservation})
        reservation.reservation_date=date
        reservation.time_slot=time
        reservation.guests=guests
        reservation.table=table
        reservation.save()
        return redirect('view_reservations')
    return render(request,'admin_modify.html',{'reservation':reservation})

