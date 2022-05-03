import json
from django.shortcuts import render, redirect, get_object_or_404
from school.forms import SelectDateForm, EnterCountForm, CreateRoomForm
from school.models import Room, Student
from django.db.models import Count
from django.db.models import Q
import django_tables2 as tables


class NameTable(tables.Table):
    room_name = tables.Column()
    students = tables.Column()


def get_students_overall():
    data = Room.objects.annotate(students=Count('seat__student'))
    return data


def get_students_by_date(date):
    data = Room.objects.annotate(students=Count('seat__student', filter=Q(seat__student__on_date=date)))
    return data


def add_room_view(request):
    rooms = []
    form = CreateRoomForm()
    message = ''
    if request.method == "POST":
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Room Created"
        else:
            message = "Error - Unable to Create Room"
        rooms = Room.objects.all()

    return render(request, 'room/add_room.html', locals())


def get_room_details(request, room_name=None):
    all_rooms = Room.objects.all()
    filtered_room = Room.objects.filter(name=room_name)
    all_students = []
    if room_name != None:
        all_students = Student.objects.filter(student_seat__seat_room__name=room_name)
    else:
        all_students = Student.objects.all()

    student_count = len(all_students)
    return render(request, 'room/room_details.html', locals())


def get_maximum_students(request):
    room_detail = []
    date_selected = "None"
    if request.method == "POST":
        req_form = SelectDateForm(request.POST)
        date_selected = request.POST['allocation_date']
        room_detail = get_students_by_date(date_selected)
    else:
        room_detail = get_students_overall()
    form = SelectDateForm()
    final_data = []
    for det in room_detail:
        data = {'room_id': det.pk, 'max_seats': det.maximum_seats, 'seated_people': det.students}
        final_data.append(data)

    final_data = json.dumps(final_data)

    return render(request, 'room/room_max_details.html', locals())


def room_with_x_students(request):
    form = EnterCountForm()
    count = 0
    room_list = []
    if request.method == "POST":
        type = int(request.POST['type'])
        count = int(request.POST['student_count'])
        if type == 1:
            data = get_students_overall()
            for v in data:
                if v.students >= count:
                    room_list.append({
                        'room_name': v.name,
                        'students': v.students
                    })
        else:
            on_date = request.POST['allocation_date']
            data = get_students_by_date(on_date)
            for v in data:
                if v.students >= count:
                    room_list.append({
                        'room_name': v.name,
                        'students': v.students
                    })
        pass
    data = NameTable(room_list)
    return render(request, 'room/room_with_x_students.html', locals())
