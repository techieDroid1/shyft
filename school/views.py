from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView
from school.forms import CreateStudentForm
from school.models import Student

'''
Not Being Used
'''

# Create your views here.
class BaseView(FormView):
    form_class = CreateStudentForm
    template_name = 'student.html'


class AddStudentView(TemplateView):
    template_name = 'add_student_result.html'

    def get_queryset(self):
        self.name = get_object_or_404(Student, name=self.kwargs['name'])
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Successf"
        return context
