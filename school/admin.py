from django import forms
from django.contrib import admin

from school.models import Student, School, Room, Seat, StudentHistory


@admin.register(StudentHistory)
class StudentHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'roll_no', 'on_date', 'student_seat', 'room', 'school', 'created', 'modified',)
    list_filter = (
        'student_seat__seat_room__room_school__name', 'student_seat__seat_room__name', 'student_seat__seat_id',
        'on_date')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    list_display = ('name', 'student_seat', 'get_seat_room')
    list_filter = (
        'student_seat__seat_room__room_school__name', 'student_seat__seat_room__name', 'student_seat__seat_id')

    class SeatChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return "%s - %s" % (obj.seat_id, obj.seat_room)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student_seat':
            return self.SeatChoiceField(queryset=Seat.objects)
        return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_seat_room(self, obj):
        return obj.student_seat.seat_room

    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    list_filter = ('room_school__name',)
    pass


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    pass


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    list_display = ('seat_id', 'seat_room',)
    list_filter = ('seat_room__room_school__name', 'seat_room__name',)
    pass
