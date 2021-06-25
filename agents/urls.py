from django.urls import path

from . import views
app_name = 'agents'
urlpatterns = [
    path('' , views.AgentListView.as_view() , name='agent_list'),
    path('create/' , views.AgentCreateView.as_view() , name='agent_create'),
    path('detail/<int:pk>' , views.AgentDetailView.as_view() , name='agent_detail'),
    path('update/<int:pk>' , views.AgentUpdateView.as_view() , name='agent_update'),
    path('delete/<int:pk>' , views.AgentDeleteView.as_view() , name='agent_delete'),

]