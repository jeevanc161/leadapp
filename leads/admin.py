from django.contrib import admin

# Register your models here.
from .models import User , Lead, Agent, UserProfile , Category , Contactus

class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'age',
        'email',
        'phone_number',
        'date_added',
    ]
    ordering = [ '-date_added']


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'organisation',
    ]
    list_filter = [ 'name' , 'organisation']

class ContactUsAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'email',
        'message'
    ]

    ordering = ['-date_created']

admin.site.register(Contactus , ContactUsAdmin)
admin.site.register(User)
admin.site.register(Lead , LeadAdmin)
admin.site.register(Agent)
admin.site.register(UserProfile)
admin.site.register(Category , CategoryAdmin)