from django.core.exceptions import ValidationError
from django.db import (
    models, OperationalError,
    IntegrityError
)
from django_extensions.db.models import TimeStampedModel


class School(TimeStampedModel):
    name = models.CharField("School Name", max_length=100)

    def __str__(self):
        return self.name


def max_seats(num):
    room = Room.objects.filter(pk=num).get()
    if room.seat_set.count() >= room.maximum_seats:
        raise ValidationError('Room Full with {} seats'.format(room.maximum_seats))


class Room(TimeStampedModel):
    name = models.CharField("Room Name", max_length=100, primary_key=True)
    maximum_seats = models.IntegerField(default=3)
    room_school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        room_data = StudentsInRoomData()
        room_data.room_name = self.name
        room_data.save()
        super(Room, self).save(**kwargs)

    def delete(self):
        # obj_to_delete = StudentsInRoomData.objects.
        super(Room, self).delete()

    def __str__(self):
        return self.name


class Seat(TimeStampedModel):
    seat_id = models.CharField("Seat ID", max_length=100)
    seat_room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE, validators=(max_seats,)
    )

    class Meta:
        unique_together = (('seat_id', 'seat_room'))

    def __str__(self):
        return self.seat_id


class Student(TimeStampedModel):
    name = models.CharField("Full Name", max_length=100)
    roll_no = models.CharField(max_length=6, unique=True, blank=True, null=True)
    on_date = models.DateField()
    student_seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE
    )
    email = models.EmailField("Email Address")

    def save(self, **kwargs):
        history = StudentHistory()

        for k, v in self.__dict__.items():
            if k != '_state' and k != 'id':
                setattr(history, k, v)
        history.room = self.student_seat.seat_room.name
        history.school = self.student_seat.seat_room.room_school.name

        history.save()
        super(Student, self).save(**kwargs)

    def delete(self, using=None, keep_parents=False):
        obj_dict = self.__dict__
        # entry =

    class Meta:
        unique_together = (('student_seat', 'on_date'))

    def __str__(self):
        return self.name


class StudentHistory(TimeStampedModel):
    name = models.CharField("Full Name", max_length=100, editable=False)
    roll_no = models.CharField(max_length=6, blank=True, null=True, editable=False)
    on_date = models.DateField(editable=False)
    student_seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE
    )
    email = models.EmailField("Email Address", editable=False)
    room = models.CharField("Room Name", max_length=100, editable=False, default="")
    school = models.CharField("School Name", max_length=100, editable=False, default="")

    def __str__(self):
        return self.name


class StudentsInRoomData(models.Model):
    room_name = models.CharField("Room Name", max_length=100, primary_key=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.room_name
