from django.views.generic import TemplateView

class DemoPage(TemplateView):
    template_name = 'test_page.html'
