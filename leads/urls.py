from django.urls import path
from . import views

app_name = 'leads'
 
urlpatterns = [
    path('' , views.LeadListView.as_view() ,  name = 'home_page'),
    path('<int:pk>/' , views.LeadDetailView.as_view() , name = 'lead_detail'),
    path('<int:pk>/update/' , views.LeadUpdateView.as_view() , name = 'lead_update'),
    path('<int:pk>/delete/' , views.LeadDeleteView.as_view() , name = 'lead_delete'),
    path('<int:pk>/assign_agent/', views.AssignAgentview.as_view() , name= 'assign_agent'),
    path('<int:pk>/category_update/', views.LeadCategoryUpdateview.as_view() , name= 'lead_category_update'),
    path('create/' , views.LeadCreateView.as_view() , name = 'lead_create'),
    path('categories/' , views.CategoryListView.as_view() , name = 'category_list'),
    path('<int:pk>/category/' , views.CategoryDetailView.as_view() , name = 'category_detail'),
    # path('delete/<int:id>' , views.lead_delete , name = 'lead_delete'),
    
]
