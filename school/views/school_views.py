from django.shortcuts import render
from school.forms import CreateSchoolForm
from school.models import School


def add_school_view(request):
    schools = []
    form = CreateSchoolForm()
    message = ''
    if request.method == "POST":
        form = CreateSchoolForm(request.POST)
        if form.is_valid():
            form.save()
            message = "School Created"
        else:
            message = "Error - Unable to Create School"
        schools = School.objects.all()

    return render(request, 'school/add_school.html', locals())
