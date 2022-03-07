# from django.views.generic import TemplateView
#
# from events.models import  Event
#
# class IndexView(TemplateView):
#     template_name = 'main/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context['events_list'] = Event.objects.all()
#         context['special_content'] = True
#         return context
