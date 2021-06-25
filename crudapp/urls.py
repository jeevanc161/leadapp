from django.urls import path
from . import views

app_name = 'crudapp'

urlpatterns = [
    path('' , views.StudentAddShowView.as_view() , name= 'addandshow'),
    path('delete/<int:id>' , views.StudentDeleteView.as_view() , name= 'deletedata'),
    path('<int:id>' , views.StudentUpdateView.as_view() , name = 'updatedata'),
]