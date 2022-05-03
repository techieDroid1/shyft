from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from school.forms import CreateStudentForm, SelectDateAndStudentForm, ChangeRoomForm
from school.models import Student, StudentHistory, Seat


def add_student_form_view(request):
    title = "Add Student"
    form = CreateStudentForm()

    return render(request, 'student/student.html', locals())


def add_student_status_view(request):
    all_students = Student.objects.all()
    message = ''
    if request.method == "POST":
        form = CreateStudentForm(request.POST)

        if form.is_valid():
            form.save()
            message = "Student Added"
        else:
            message = form.errors

        all_students = Student.objects.filter(student_seat=request.POST['student_seat'])

    context = {
        'message': message,
        'students': all_students
    }
    return render(request, 'student/add_student_result.html', locals())


def student_position_on_date(request):
    title = "Student Position on Date"
    # all_students = Student.objects.all()
    form = SelectDateAndStudentForm()
    student_history = []
    if request.method == "POST":
        selected_roll_number = request.POST['student']
        selected_date = request.POST['allocation_date']
        student_history = StudentHistory.objects.filter(roll_no=selected_roll_number, on_date=selected_date)

    return render(request, 'student/student_position.html', locals())


def change_student_room(request):
    title = "Change Student Room"
    form = ChangeRoomForm()
    message = ""
    if request.method == "POST":
        student = Student.objects.filter(roll_no=request.POST['student'])
        seat = Seat.objects.filter(seat_id=request.POST['seat'])
        obj = student[0]
        obj.on_date = request.POST['allocation_date']
        obj.student_seat = seat[0]
        print(obj)
        try:
            obj.save()
            message = "Success"
        except:
            message = "Error"

    return render(request, 'student/change_room.html', locals())

