import random
from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin


class AgentListView(OrganisorAndLoginRequiredMixin , generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin , generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent_list')


    def form_valid(self, form):
        user =  form.save(commit=False)
        user.is_organisation = False
        user.is_agent = True
        user.set_password(f"{random.randint(0,100000)}")
        user.save()
        Agent.objects.create(
            user = user,  
            organisation = self.request.user.userprofile
        )

        send_mail(
            subject='Welcome to the Jeevan CRM Managment Sysmtem',
            message=f'Hello ' + f'{user.first_name} ,'  +
                '\r\nYour username is : ' + f'{user.username} '+
                '''\r\nYou are invited as the Agent.Please Open the Jeevan CRM Web App and reset your password with this username.
                Thank you 
                Best Regards
                Jeevan CRM System''',
            from_email='jeevanc162@gmail.com',
            recipient_list=[user.email]
        )
        return super(AgentCreateView , self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin , generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent' 

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)



class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm
  
    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        agent = Agent.objects.get(id = self.kwargs['pk'])
        # organisation = self.request.user.userprofile
        return agent.user.all()



class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_success_url(self):
        return reverse('agents:agent_list')

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

