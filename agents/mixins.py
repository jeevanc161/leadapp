from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganisorAndLoginRequiredMixin(AccessMixin):
    """
    Verifiy that the current user is athenticate and is an Organisor
    """
    def dispatch(self, request , *args , **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisation:
            return redirect('leads:home_page')
        return super().dispatch(request , *args , **kwargs) 