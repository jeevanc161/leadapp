from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import fields
from .models import Agent, Category, Lead

User = get_user_model()

#create Form using  Form Class
# class LeadForm(forms.Form):
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#     age = forms.IntegerField(min_value=0)

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        # fields = '__all__'
        fields = {
            'first_name',
            'last_name',
            'age',
            'email',
            'phone_number',
            'description',

        }
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control'}), 
            'age' : forms.NumberInput(attrs={'class' : 'form-control'}), 
            'agent' : forms.Select(attrs={'class' : 'form-control'}),  
        }

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username',]
        field_classes  = {'username' : UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(
        queryset = Agent.objects.none()
    )
    
    def __init__(self , *args,  **kwargs):
        request  = kwargs.pop('request')
        super(AssignAgentForm, self).__init__(*args , **kwargs)
        agent = Agent.objects.filter(organisation = request.user.userprofile)
        self.fields['agent'].queryset = agent


class LeadCategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = {
            'category',
        }