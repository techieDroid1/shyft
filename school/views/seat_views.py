from django.shortcuts import render
from school.forms import AddSeatForm
from school.models import Seat


def add_seat_view(request):
    seats = []
    form = AddSeatForm()
    message = ''
    if request.method == "POST":
        form = AddSeatForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Seat Added"
        else:
            message = "Error - Unable to Add Seat"
        seats = Seat.objects.all()

    return render(request, 'seat/add_seat.html', locals())
