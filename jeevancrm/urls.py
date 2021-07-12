from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import ( 
    LoginView, 
    LogoutView, 
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path , include
from leads import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.LandingPageView.as_view() , name = 'landing-page'),
    path('about/' , views.AboutPageView.as_view() , name = 'about_page'),
    path('service/' , views.ServicePageView.as_view() , name = 'service_page'),
    path('contact/' , views.ContactPageView.as_view() , name = 'contact_page'),
    path('leads/' , include('leads.urls' , namespace = 'leads')),
    path('agent/' , include('agents.urls' , namespace = 'agents')),
    # path('crudapp/' , include('crudapp.urls' , namespace = 'crudapp'))
    path('login/' , LoginView.as_view() , name='login'),
    path('logout/' , LogoutView.as_view() , name='logout'),
    path('reset-password/' , PasswordResetView.as_view() , name= 'reset-password'),
    path('password-reset-done/' , PasswordResetDoneView.as_view() , name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/' , PasswordResetConfirmView.as_view() , name='password_reset_confirm'),
    path('password-reset-complete/' , PasswordResetCompleteView.as_view() , name='password_reset_complete'),
    path('signup/' , views.SignupView.as_view() , name = 'signup')
]

urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)