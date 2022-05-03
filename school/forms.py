import datetime
from django import forms
from school.models import Student, Room, Seat, School
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


def get_student_choices():
    students = Student.objects.all()
    STUDENT_CHOICES = []
    for student in students:
        tp = (student.roll_no,
              "{} -||- {} -||- {} -||- {}".format(student.name, student.roll_no, student.student_seat.seat_id,
                                                  student.student_seat.seat_room.name))
        STUDENT_CHOICES.append(tp)
    return tuple(STUDENT_CHOICES)


def get_room_choices():
    rooms = Room.objects.all()
    ROOM_CHOICES = []
    for room in rooms:
        tp = (room.name, room.name)
        ROOM_CHOICES.append(tp)
    return tuple(ROOM_CHOICES)


def get_seat_choices():
    seats = Seat.objects.all()
    SEAT_CHOICES = []
    for seat in seats:
        tp = (seat.seat_id, "{} -||- {}".format(seat.seat_id, seat.seat_room))
        SEAT_CHOICES.append(tp)
    return tuple(SEAT_CHOICES)


class CreateStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('add_student')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ()
        widgets = {
            'on_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class CreateRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('add_room')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Room
        fields = '__all__'


class AddSeatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('add_seat')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Seat
        fields = '__all__'


class CreateSchoolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('add_school')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = School
        fields = '__all__'


class SelectDateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('get_maximum')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    allocation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class SelectDateAndStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('get_student_on_date')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    STUDENT_CHOICES = get_student_choices()
    allocation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    student = forms.ChoiceField(
        choices=STUDENT_CHOICES
    )


class ChangeRoomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('change_room')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    STUDENT_CHOICES = get_student_choices()
    ROOM_CHOICES = get_room_choices()
    SEAT_CHOICES = get_seat_choices()
    student = forms.ChoiceField(
        choices=STUDENT_CHOICES
    )
    allocation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    seat = forms.ChoiceField(
        choices=SEAT_CHOICES
    )


class EnterCountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('room_with_x')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    CHOICES = [('1', 'Overall'), ('2', 'On Particular Date')]
    type = forms.CharField(label='Date', widget=forms.RadioSelect(choices=CHOICES))
    allocation_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput(attrs={'type': 'date'}))
    student_count = forms.IntegerField(label="Number of Students", initial=15)
