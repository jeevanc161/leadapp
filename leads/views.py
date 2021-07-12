from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.shortcuts import render , redirect , reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic 
from .models import Lead , Category
from .forms import LeadForm , CustomUserCreationForm ,AssignAgentForm , LeadCategoryUpdateForm, ContactUsForm
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.contrib import messages
# CRUD+L -- Create, Retrive , Update , Delete , List


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = 'landing_page.html'

class AboutPageView(generic.TemplateView):
    template_name = 'about.html'

class ServicePageView(generic.TemplateView):
    template_name = 'service.html'


class ContactPageView(generic.TemplateView):
    template_name = 'contact.html'
    
    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(**kwargs)
        form = ContactUsForm()
        context = {'form' : form}
        return context

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your message has been sent. Thank you!")
            return redirect('/contact')
def landing_page(request):
    return render(request , 'landing_page.html')

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name  = 'leads'

    def get_queryset(self):
        user = self.request.user

        if user.is_organisation:
            queryset = Lead.objects.filter(
                organisation = user.userprofile,
                # agent__isnull = False
            )
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            queryset = Lead.objects.filter(agent__user = user)
        return queryset

    # def get_context_data(self, **kwargs):
    #     user = self.request.user
    #     context =  super(LeadListView , self).get_context_data(**kwargs)
    #     if user.is_organisation:
    #         queryset = Lead.objects.filter(
    #             organisation = user.userprofile , 
    #             agent__isnull = True)
    #         context.update({
    #             'unassigned_leads': queryset
    #         })
    #     return context

    def get_context_data(self, **kwargs):
        context =  super(LeadListView , self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisation:
            total_leads = Lead.objects.filter(
                organisation = user.userprofile).count()
        else:
            total_leads = Lead.objects.filter(agent__user = user).count()
        context.update({
            'total_leads': total_leads
        })
        return context

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads' : leads
    }
    return render(request , 'leads/lead_list.html', context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name  = 'lead' 

    def get_queryset(self):
        user = self.request.user

        if user.is_organisation:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            queryset = Lead.objects.filter(agent__user = user)
        return queryset


def lead_detail(request , id):
    lead = Lead.objects.get(id = id)
    context = {
        'lead': lead
        }
    return render(request , 'leads/lead_detail.html', context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadForm

    def get_success_url(self):
        return reverse('leads:home_page')

    def form_valid(self , form):
        # TO DO send email 
        # send_mail(
        #     subject = 'A lead has been created',
        #     message='Go to the site and check out the list',
        #     from_email='jeevanc162@gmail.com',
        #     recipient_list=[],

        # )
        return super(LeadCreateView , self).form_valid(form)

def lead_create(request):
    form = LeadForm()
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form' : form 
    }
    return render(request , 'leads/lead_create.html' , context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadForm

    def get_success_url(self):
        return reverse('leads:home_page')

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)


def lead_update(request , id):
    lead = Lead.objects.get(id=id)
    form = LeadForm(instance=lead)
    if request.method == 'POST':
        form = LeadForm(request.POST , instance=lead )
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form' : form 
    }
    return render(request , 'leads/lead_update.html' , context)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse('leads:home_page')

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)


def lead_delete(request , id):

    
    lead = Lead.objects.get(id=id)
    lead.delete()
    return redirect('/leads')

class AssignAgentview(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm
    
    def get_success_url(self):
        return reverse('leads:home_page')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentview, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id = self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentview , self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name  = 'category_list'
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView , self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisation:
            queryset = Lead.objects.filter(
                organisation = user.userprofile,
            )
        else:
            queryset = Lead.objects.filter(
                organisation = user.agent.organisation
            )
        context.update({
            'unassign_leads': queryset.filter(category__isnull=True).count()
        })
        return context


    def get_queryset(self):
        user = self.request.user

        if user.is_organisation:
            queryset = Category.objects.filter(
                organisation = user.userprofile,
            )
        else:
            queryset = Category.objects.filter(
                organisation = user.agent.organisation
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin , generic.DetailView):

    template_name = 'leads/cetegory_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user

        if user.is_organisation:
            queryset = Category.objects.filter(
                organisation = user.userprofile,
            )
        else:
            queryset = Category.objects.filter(
                organisation = user.agent.organisation
            )
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView , self).get_context_data(**kwargs)
    #     # leads  = Lead.objects.filter(category = self.get_object())
    #     leads = self.get_object().leads.all()

    #     context.update({
    #         'leads': leads
    #     })
    #     return context 

class LeadCategoryUpdateview(LoginRequiredMixin , generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm


    def get_queryset(self):
        user = self.request.user
        if user.is_organisation:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            # queryset = Lead.objects.filter(agent__user = user)
        return queryset
    
    def get_success_url(self):
        return reverse('leads:lead_detail', kwargs = {'pk': self.get_object().id})
