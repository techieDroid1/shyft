from django.urls import path
from school.views import student_views, room_views, home_view, school_views, seat_views

urlpatterns = [
    path('', home_view.home_view, name='homepage'),
    path('student/', student_views.add_student_form_view, name='student'),
    path('add/room/', room_views.add_room_view, name='add_room'),
    path('add/seat/', seat_views.add_seat_view, name='add_seat'),
    path('add/school/', school_views.add_school_view, name='add_school'),
    path('change/room/', student_views.change_student_room, name='change_room'),
    path('get/student/', student_views.student_position_on_date, name='get_student_on_date'),
    path('add/', student_views.add_student_status_view, name='add_student'),
    path('room/maximum/', room_views.get_maximum_students, name='get_maximum'),
    path('room/maximum/<date>/', room_views.get_maximum_students, name='get_maximum_on_date'),
    path('room/', room_views.get_room_details, name='all_room_details'),
    path('room/<room_name>/', room_views.get_room_details, name='room_details'),
    path('room/with/x/', room_views.room_with_x_students, name='room_with_x'),
]
