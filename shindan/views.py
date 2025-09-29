from django.views.generic import TemplateView

class shindanView(TemplateView):
    template_name = 'shindan/shindan.html'
    
class afterboughtView(TemplateView):
    template_name = 'afterbought/afterbought.html'