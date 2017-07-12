from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from crawl.models import Workout

# Create your views here.

class IndexView(generic.ListView):
    # queryset = Workout.objects.all() is the long form of model = Workout
    queryset = Workout.objects.all().order_by('-date')
    template_name = 'browse/index.html'
    context_object_name = 'workout_list'
    paginate_by = 8

class WorkoutDetailView(generic.DetailView):
    model = Workout
    template_name = 'browse/workoutdetail.html'

    def get_pretty_results(self, uom, benchmark_list):
        # Timed results are stored as decimals. Convert to minutes:seconds.
        if 'time' in uom and benchmark_list:
            for gender in benchmark_list:
                gender.min_score = "{}:{:02.0f}".format(int(gender.min_score), gender.min_score % 1 * 60) 
                gender.avg_score = "{}:{:02.0f}".format(int(gender.avg_score), gender.avg_score % 1 * 60)
                gender.max_score = "{}:{:02.0f}".format(int(gender.max_score), gender.max_score % 1 * 60)
        else:
            for gender in benchmark_list:
                gender.min_score = "{:.0f}".format(gender.min_score) 
                gender.avg_score = "{:.0f}".format(gender.avg_score)
                gender.max_score = "{:.0f}".format(gender.max_score)
        # Make gender readable
        gender_key = {"F":"Female","M":"Male","E":"Not Specified"}
        for gender in benchmark_list: gender.gender = gender_key[gender.gender]
        return benchmark_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WorkoutDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet for benchmarks
        context['benchmark_list'] = context['workout'].benchmark_set.all()
        # Change format of results for better readability
        context['benchmark_list'] = self.get_pretty_results(context['workout'].uom, context['benchmark_list'])
        return context

class AboutView(generic.TemplateView):
    template_name = 'browse/about.html'

class ContactView(generic.TemplateView):
    template_name = 'browse/contact.html'
