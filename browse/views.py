from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from crawl.models import Workout

# Create your views here.

class IndexView(generic.ListView):
    model = Workout
    template_name = 'browse/index.html'

class WorkoutDetailView(generic.DetailView):
    model = Workout
    template_name = 'browse/workoutdetail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WorkoutDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet for benchmarks
        context['benchmark_list'] = context['workout'].benchmark_set.all()
        return context
