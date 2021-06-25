from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from .form import StudentRegistration
from .models import Student
from django.views.generic.base import TemplateView , RedirectView
from django.views import View

class StudentAddShowView(TemplateView):
    template_name = 'crudapp/addandshow.html'

    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(**kwargs)
        form = StudentRegistration()
        students = Student.objects.all().order_by('-id')[:5] 
        context = {'students' : students , 'form' : form}
        return context
    
    def post(self, request):
        form = StudentRegistration(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # reg = Student(name=name , email=email, password=password)
            form.save()
            return redirect('/crudapp')

class StudentDeleteView(RedirectView): 
    url = '/crudapp'  
    def get_redirect_url(self , *args , **kwargs):
        print(kwargs)
        del_id = kwargs['id']
        Student.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)

class StudentUpdateView(View):
    
    def get(self , request ,id, *args , **kwargs):
        student  = Student.objects.get(pk = id)
        form = StudentRegistration(instance=student)
        return render(request , 'crudapp/updatestudent.html' , {'form':form })

    def post(self , request , id):
        student = Student.objects.get(pk=id)
        form = StudentRegistration(request.POST , instance = student)
        if form.is_valid():
            form.save()
            return redirect('/crudapp')

